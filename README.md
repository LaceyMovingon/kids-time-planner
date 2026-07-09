# Kids Time Planner

> 基于 xiaozhi-esp32-server 的儿童学习陪伴 Agent
> Fork 自 [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)

## 项目简介

为 7-12 岁儿童设计的学习生活陪伴 Agent，运行在 ESP32 硬件 + 自建后端之上。

| 维度 | 说明 |
|------|------|
| **目标用户** | 锅盖（小学 3 年级，8 岁） |
| **硬件** | ESP32-S3 + 麦克风 + 扬声器 |
| **后端** | 本仓库 (kids-time-planner) |
| **核心能力** | 时间规划 / 学习陪伴 / 错题本 / 家长护栏 |
| **理论依据** | SDT（自我决定理论）：自主选择 + 胜任感 + 联结 |

## 与 openclaw 版的差异

| 维度 | openclaw 版（外挂） | 本项目（自建） |
|------|-------------------|---------------|
| 架构 | xiaozhi + OpenClaw 双 Agent | 单一 Agent 进程 |
| 通信 | 三段 WebSocket 串联 | 一段 WebSocket + HTTP API |
| 首字延迟 | 5-6 秒 | 目标 < 3 秒 |
| 路由 | 硬编码（唤醒词/关键词） | 单一路径，Prompt 决定能力 |
| 可观测性 | 分散在两个系统 | 统一埋点 + 指标 |

## 自建模块（M1-M5）

- **M1 个性化 Prompt** - 动态注入孩子画像
- **M2 跨会话记忆** - SQLite + 画像系统
- **M3 教材 RAG** - Chroma + BGE 向量检索
- **M4 MCP 工具** - 错题本/提醒/日程
- **M5 护栏与可观测** - 时长限制 + 成本统计

## 快速开始

```bash
# 1. 装依赖
cd main/xiaozhi-server
pip install -r requirements.txt

# 2. 配置
mkdir -p data && cp config.yaml data/.config.yaml
# 编辑 data/.config.yaml 填入 LLM API Key

# 3. 启动
python app.py
```

## 文档

- 技术方案：`../docs/agent-design.md`
- openclaw 反例分析：`../docs/kids-time-planner — xiaozhi-server 模块改动清单.md`

## 状态

项目初始化中...

## License

继承上游 Apache 2.0。
