# QQ 官方机器人配置与接入指南

本指南手把手教你如何在 `yukichan-bot-v2` 中申请并接入 QQ 官方机器人适配器（`nonebot-adapter-qq`）。

---

## 目录

1. [前置准备：申请 QQ 官方机器人](#1-前置准备申请-qq-官方机器人)
2. [配置环境变量 (.env)](#2-配置环境变量-env)
3. [事件权限与沙箱设置](#3-事件权限与沙箱设置)
4. [启动与测试机器人](#4-启动与测试机器人)
5. [常见问题与排查](#5-常见问题与排查)

---

## 1. 前置准备：申请 QQ 官方机器人

1. 访问 [QQ 开放平台](https://q.qq.com/) 并使用 QQ 账号登录。
2. 进入 **控制台** -> **应用管理**，点击 **创建应用**（选择机器人应用）。
3. 完成机器人基本信息填写（名称、头像、简介等）。
4. 在机器人应用详情页面的 **开发** -> **开发设置** 中，获取以下凭据：
   - **机器人 ID (`App ID`)**
   - **机器人 Token (`App Token`)**
   - **机器人 Secret (`App Secret`)**

---

## 2. 配置环境变量 (.env)

在项目根目录下，复制 `.env.example` 生成 `.env` 配置文件：

```bash
cp .env.example .env
```

打开 `.env` 文件，取消 QQ 官方适配器相关配置的注释，并填入从开放平台获取的凭据：

```ini
# 驱动与监听配置
DRIVER=~fastapi+~httpx+~websockets
HOST=127.0.0.1
PORT=8080

# QQ 官方机器人配置
# 开发调试阶段建议开启沙箱模式（true），上线投产后改为 false
QQ_IS_SANDBOX=true

# 机器人凭据列表 (JSON 字符串格式)
QQ_BOTS='[{"id":"102000000","token":"YourAppTokenHere","secret":"YourAppSecretHere","intent":{"c2c_group_at_messages":true}}]'
```

> **参数说明：**
> - `id`: 开放平台获取的机器人 App ID（字符串形式）。
> - `token`: 开放平台获取的机器人 App Token。
> - `secret`: 开放平台获取的 App Secret。
> - `intent`: 事件订阅掩码/配置。设置 `c2c_group_at_messages: true` 表示订阅单聊（C2C）与群聊中的 @ 机器人消息。

---

## 3. 事件权限与沙箱设置

### 3.1 沙箱环境配置
在开发阶段，QQ 官方机器人需要通过沙箱环境进行测试：
1. 在开放平台后台进入 **开发** -> **沙箱配置**。
2. 将你的个人 QQ 号、测试频道或测试 QQ 群加入沙箱白名单。
3. 确保 `.env` 中的 `QQ_IS_SANDBOX=true`。

### 3.2 权限与 Intent 申请
1. 在开放平台后台 **功能** -> **事件订阅** 中，确保勾选了所需的事件权限：
   - **群聊与单聊消息**（C2C & 群聊 @ 消息）
   - **频道消息**（如需在 QQ 频道中使用）
2. 机器人默认在群聊中仅响应 `@机器人` 的消息，请确保测试时包含了 `@` 提醒。

---

## 4. 启动与测试机器人

使用 `uv` 运行机器人：

```bash
uv run python bot.py
```

终端输出类似如下日志即表示成功连接至 QQ 开放平台 OpenAPI：

```text
[INFO] nonebot | Yielding Driver (FastAPI + HTTPX + WebSockets)...
[INFO] nonebot | Loading plugins: ['src/yukichan_bot/plugins']
[INFO] nonebot | Loaded plugin: match
[INFO] nonebot | Loaded plugin: chess
[INFO] nonebot | Connected to QQ OpenAPI ...
```

### 触发测试：
1. **测试 `match` 插件**：在已配置沙箱的群/私聊中发送：
   ```text
   @机器人 老婆
   ```
   机器人将回复：`肥宅不要乱叫老婆啊！`

2. **测试 `chess` 插件**：在已配置沙箱的群中发送：
   ```text
   @机器人 下棋
   ```
   机器人将创建棋盘对局并返回回复。

---

## 5. 常见问题与排查

| 现象 / 报错 | 可能原因 | 解决办法 |
| --- | --- | --- |
| `4001 validation failed` 或连接断开 | App ID / Token / Secret 填写错误 | 仔细核对开放平台后台凭据，确保无多余空格 |
| 机器人对群消息没有响应 | 1. 消息未 `@机器人`<br>2. 个人/群未加入沙箱名单<br>3. `intent` 配置缺失 | 1. 确保发送格式为 `@机器人 指令`<br>2. 在开放平台后台将 QQ 号/群加入沙箱名单<br>3. 检查 `.env` 中的 `intent` 配置 |
| 图片无法发送 / 显示失败 | QQ 开放平台富媒体发送权限受限 | 确保开放平台已开启富媒体/图片发送权限，且图片格式正常 |
