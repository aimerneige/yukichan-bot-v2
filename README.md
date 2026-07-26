# yukichan-bot-v2

[![NoneBot2](https://img.shields.io/badge/NoneBot-v2.5+-red.svg)](https://nonebot.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPLv3-green.svg)](LICENSE)

基于 [NoneBot2](https://nonebot.dev/) 重建的 `yukichan-bot` 新版本。

## 核心特性

- **跨平台适配**：同时支持 OneBot V11 协议（面向 LLOneBot、NapCat 等）以及 QQ 官方机器人协议。
- **双适配器统一架构**：业务插件复用同一个逻辑接口，避免按平台重复编写匹配逻辑。
- **现代化依赖管理**：推荐使用 [uv](https://github.com/astral-sh/uv) 进行高效的 Python 依赖安装与管理。

---

## 插件与功能列表

| 插件 | 触发指令 / 条件 | 功能说明 |
| --- | --- | --- |
| **`match`** | `老婆` | 精确匹配基础回复 |
| **`chess`** | `国际象棋` / `对弈` / `认输` 等 | 国际象棋对弈插件（支持人机与双人对弈） |
| **`tarot`** | `运势预测` / `塔罗占卜` / `抽塔罗牌` / `塔罗` | 塔罗牌抽牌与占卜解牌 |
| **`fadian`** | `每日发癫 [名字]` / `小作文` / `发大病` | 随机发癫文案及长小作文生成 |
| **`fortune`** | `求签 <事项>` | 根据日期与用户 ID 哈希生成今日求签运势 |
| **`random`** | `掷硬币` (`/coin`) / `只因币` / `掷骰子` (`/dice`) / `抽扑克` (`/card`) | 掷硬币、骰子、抽扑克牌及音频片段发送 |
| **`read60s`** | `今日新闻` / `早报` / `60s` | 异步获取 60s 读懂世界新闻早报图片 |
| **`suangua`** | `算卦 [事项]` | 周易 64 卦占卦及卦象图文解析 |

---

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10+ 及 `uv` 依赖管理工具。

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置文件 setup

复制 `.env.example` 并重命名为 `.env`，配置所需适配器与监听端口：

```bash
cp .env.example .env
```

### 4. 运行机器人

```bash
uv run python bot.py
```

### 5. 运行单元测试

```bash
uv run pytest
```

---

## 项目结构

```text
yukichan-bot-v2/
├── src/
│   └── yukichan_bot/
│       └── plugins/       # 业务插件目录
│           ├── chess/
│           ├── fadian/
│           ├── fortune/
│           ├── match/
│           ├── random/
│           ├── read60s/
│           ├── suangua/
│           └── tarot/
├── tests/                 # 单元测试目录
├── bot.py                 # Bot 启动入口
├── pyproject.toml         # 项目配置与依赖说明
└── README.md
```
