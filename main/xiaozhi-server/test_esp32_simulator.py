"""
ESP32 模拟客户端 - 验证 xiaozhi-esp32-server 端到端链路

模拟 ESP32 设备：
1. HTTP GET OTA 接口，拿到 WebSocket URL
2. WebSocket 连入，发送 hello（设备标识）
3. 接收后端的 hello 响应（包含 audio_params）
4. 可选：发送一段 opus 音频帧，观察 ASR/LLM/TTS 链路

用法: venv/bin/python test_esp32_simulator.py
"""
import asyncio
import json
import sys
import websockets
import httpx


OTA_URL = "http://192.168.0.101:8003/xiaozhi/ota/"
# 模拟 ESP32 的 headers
ESP32_HEADERS = {
    "device-id": "90:70:69:35:f7:1c",  # 模拟锅盖的 ESP32 MAC
    "client-id": "11:22:33:44:55:66",
    "User-Agent": "xiaozhi-esp32/2.0",
}


async def fetch_ota():
    """1. 调 OTA 接口拿 WebSocket 地址"""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OTA_URL, headers=ESP32_HEADERS)
        r.raise_for_status()
        data = r.json()
        print(f"[OTA] response: {json.dumps(data, ensure_ascii=False)}")
        return data


async def connect_and_hello(ws_url):
    """2. WebSocket 连入 + 设备 hello"""
    print(f"\n[WS] connecting to {ws_url} ...")
    async with websockets.connect(
        ws_url,
        additional_headers=ESP32_HEADERS,
        max_size=10 * 1024 * 1024,
    ) as ws:
        # 设备发送 hello（参考设备固件 helloHandle.py 的消息格式）
        hello_msg = {
            "type": "hello",
            "version": 2,
            "features": {"mcp": True},
            "transport": "websocket",
            "audio_params": {
                "format": "opus",
                "sample_rate": 16000,
                "channels": 1,
                "frame_duration": 60,
            },
        }
        await ws.send(json.dumps(hello_msg))
        print(f"[WS] sent hello: {json.dumps(hello_msg)}")

        # 接收后端响应
        try:
            for i in range(5):
                msg = await asyncio.wait_for(ws.recv(), timeout=10)
                if isinstance(msg, bytes):
                    print(f"[WS] received {len(msg)} bytes (audio frame)")
                else:
                    data = json.loads(msg)
                    print(f"[WS] received: {json.dumps(data, ensure_ascii=False)[:200]}")
                    # 找到 hello 响应就 break
                    if data.get("type") == "hello":
                        print(f"\n[OK] 后端接受了设备 hello!")
                        print(f"     audio_params: {data.get('audio_params')}")
                        break
        except asyncio.TimeoutError:
            print("[WS] timeout waiting for response")


async def main():
    print("=" * 60)
    print("ESP32 Simulator - xiaozhi-esp32-server 端到端验证")
    print("=" * 60)

    # 步骤 1: 拉 OTA
    ota_resp = await fetch_ota()

    # 真实环境下 OTA 返回 {"websocket": {"url": "ws://..."}}
    # 我们的 ota_handler 当前只返回 status ok（参考 ota_handler.py）
    # 所以这里手动从日志里知道 ws URL
    ws_url = "ws://192.168.0.101:8000/xiaozhi/v1/"
    print(f"\n[INFO] 使用后端 WebSocket URL: {ws_url}")
    print("       （实际由 OTA 接口下发，当前自建后端 hardcode 在启动日志）")

    # 步骤 2: 连接 + hello
    try:
        await connect_and_hello(ws_url)
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
