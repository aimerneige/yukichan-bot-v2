# yukichan-bot-v2

[![NoneBot2](https://img.shields.io/badge/NoneBot-v2.5+-red.svg)](https://nonebot.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPLv3-green.svg)](LICENSE)

基于 [NoneBot2](https://nonebot.dev/) 重建的 `yukichan-bot` 新版本。

## 🌟 核心特性

- **跨平台适配**：同时原生支持 **OneBot V11 协议**（面向 LLOneBot、NapCat、Lagrange 等）以及 **QQ 官方机器人协议**。
- **双适配器统一架构**：业务插件复用同套逻辑接口，根据发送平台自动匹配适宜的消息段（如 At/Mention、图片、语音消息段）。
- **纯 Python 高性能渲染引擎**：告别 v1 依赖系统外部命令 `inkscape` 和外部 `pgn2gif` 脚本的模式，全面升级为 `python-chess` + `cairosvg` + `Pillow` 纯内存渲染与 GIF 合成，跨平台部署更轻量高效。
- **动态插件配置开关**：支持通过配置文件自由开启或禁用指定插件，支持新增插件自动探测与持久化配置。
- **现代化依赖管理**：使用 [uv](https://github.com/astral-sh/uv) 进行高效的 Python 依赖与虚拟环境管理。

---

## 🧩 插件与功能列表

| 插件名 | 触发指令 / 规则 | 功能说明 | 权限要求 |
| --- | --- | --- | --- |
| **`chess`** | `下棋` (`chess`), `盲棋` (`blind`), `![move]`, `认输` (`resign`), `和棋` (`draw`), `中断` (`abort`), `排行榜` (`ranking`), `等级分` (`rate`), `clean.rate` / `清空等级分`, `pgn2gif`, `lichess.org` 链接, `cheese` | 国际象棋对弈系统，支持双人对弈、盲棋模式、彩蛋主题、自动生成对局 GIF 及 ELO 等级分排行榜 | `中断`需管理员/SuperUser；`清空等级分`需 SuperUser |
| **`tarot`** | `运势预测` / `塔罗占卜` / `抽塔罗牌 [数量]` / `塔罗` | 塔罗牌抽牌与占卜系统，支持单张预测、三张阵位占卜、自定义抽牌数及正逆位自动旋转解牌 | 所有人 |
| **`fadian`** | `每日发癫 [名字]` / `小作文` / `发大病` | 随机发癫文案生成及长篇小作文发送 | 所有人 |
| **`fortune`** | `求签 <事项>` | 基于日期与用户 ID 哈希生成的每日求签运势占卜 | 所有人 |
| **`suangua`** | `算卦 [事项]` | 周易 64 卦占卦及卦象图文解析 | 所有人 |
| **`random`** | `掷硬币` (`/coin`) / `只因币` / `掷骰子` (`/dice`) / `抽扑克` (`/card`) | 随机掷硬币、只因语音片段、掷骰子及抽扑克牌 | 所有人 |
| **`read60s`** | `今日新闻` / `早报` / `60s` | 异步获取并发送每日 60s 读懂世界新闻早报图片 | 所有人 |
| **`alipay`** | `支付宝到账 <金额>` / `alipay <金额>` | 伪造生成支付宝音频到账语音消息 | 所有人 |
| **`match`** | `老婆` / `关于` (`about`) | 关键词精确匹配回复及机器人版权与捐赠信息展示 | 所有人 |
| **`ytdlp`** | `/yt-dlp <URL>` / `yt-dlp <URL>` | 异步解析并下载音视频文件上传至群聊或本地 | 仅 SuperUser |

---

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.10+ 及 [uv](https://github.com/astral-sh/uv) 依赖管理工具。

### 2. 安装依赖

```bash
uv sync
```

### 3. 环境配置 (`.env`)

复制 `.env.example` 并重命名为 `.env`，根据所使用的适配器配置参数：

```bash
cp .env.example .env
```

`.env` 配置项说明：

* **OneBot V11 配置**（使用 LLOneBot / NapCat / Lagrange 等）：
  ```env
  DRIVER=~fastapi+~httpx+~websockets
  HOST=127.0.0.1
  PORT=8080
  # 反向 WebSocket 地址配置
  ONEBOT_WS_URLS=["ws://127.0.0.1:8081"]
  ```

* **QQ 官方机器人配置**：
  ```env
  QQ_IS_SANDBOX=true
  QQ_BOTS='[{"id":"app_id","token":"app_token","secret":"app_secret","intent":{"c2c_group_at_messages":true}}]'
  ```

### 4. 插件开关配置 (`data/plugins_config.json`)

本项目支持通过配置文件控制插件的开启与禁用。配置文件路径为：`data/plugins_config.json`。

* **如果文件不存在**：机器人首次启动时会自动创建 `data/` 目录与 `plugins_config.json` 文件，并自动扫描当前所有插件，默认将它们全部设为开启（`true`）。
* **自动检测新插件**：后续若新增插件，启动时会自动在配置文件中追加新插件并默认设为 `true`。

#### 配置文件示例 (`data/plugins_config.json`)：

```json
{
  "alipay": true,
  "chess": true,
  "fadian": true,
  "fortune": true,
  "match": true,
  "random": true,
  "read60s": true,
  "suangua": true,
  "tarot": true,
  "ytdlp": true
}
```

如需禁用某个插件（例如禁用 `ytdlp`），只需将其设置为 `false` 并重启机器人即可。被禁用的插件不会加载入内存，也不会响应任何指令。

### 5. 运行机器人

```bash
uv run python bot.py
```

### 6. 运行单元测试

```bash
uv run pytest
```

---

## 📁 项目结构

```text
yukichan-bot-v2/
├── data/                  # 本地数据目录 (数据库及插件配置文件)
│   ├── chess/chess.db
│   └── plugins_config.json
├── src/
│   └── yukichan_bot/
│       ├── plugin_loader.py  # 配置驱动的插件动态加载器
│       └── plugins/          # 业务插件目录
│           ├── alipay/
│           ├── chess/
│           ├── fadian/
│           ├── fortune/
│           ├── match/
│           ├── random/
│           ├── read60s/
│           ├── suangua/
│           ├── tarot/
│           └── ytdlp/
├── tests/                 # 单元测试目录
├── bot.py                 # Bot 启动主入口
├── pyproject.toml         # 项目配置与依赖声明
└── README.md
```
