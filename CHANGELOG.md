# Changelog

## 2026-07-09 - 项目初始化

### 重构说明

本项目 fork 自 [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)，在原版基础上做以下重构：

#### 架构调整
- **去除 OpenClaw 外挂依赖** —— 单一 Agent 进程，所有能力内化
- **简化 LLM 路由** —— 删除双路径硬编码路由，LLM 走单一 Provider
- **通信链路收敛** —— ESP32 ↔ 后端 一段 WebSocket，外部 API 走 HTTP

#### 新增模块
- M1 个性化 Prompt 管理器
- M2 跨会话记忆系统
- M3 教材 RAG（Chroma + BGE）
- M4 MCP 业务工具
- M5 护栏与可观测

#### 计划优化
- 首字延迟从 5-6s 降到 < 3s
- 端到端全异步，IO 全部 await
- 流式响应：LLM 流式 + TTS 流式 + 边生成边播放

#### 待办
- [ ] 改造 LLM Provider (P0)
- [ ] 注入 M1 动态 Prompt (P0)
- [ ] 实现 M2 记忆系统 (P1)
- [ ] 实现 M3 RAG (P2)
- [ ] 实现 M4 工具集 (P1)
- [ ] 实现 M5 护栏与可观测 (P1)
