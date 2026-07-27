import json
import os
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.adapters.qq import Adapter as QQAdapter


def load_bot_certificate() -> dict:
    config_path = Path(os.getenv("BOT_CONFIG", "./botcertificate.json"))
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def map_to_nonebot_config(cert: dict) -> dict:
    """将 botcertificate.json 的结构映射为 NoneBot2 所需的配置键名。"""
    nb_config: dict = {}
    if qq := cert.get("qq"):
        if bots := qq.get("bots"):
            nb_config["qq_bots"] = bots
        if (is_sandbox := qq.get("is_sandbox")) is not None:
            nb_config["qq_is_sandbox"] = is_sandbox
    if onebot := cert.get("onebot"):
        if ws_urls := onebot.get("ws_urls"):
            nb_config["onebot_ws_urls"] = ws_urls
    return nb_config


def main() -> None:
    cert = load_bot_certificate()
    nb_config = map_to_nonebot_config(cert)
    nonebot.init(**nb_config)

    driver = nonebot.get_driver()
    driver.register_adapter(OneBotV11Adapter)
    driver.register_adapter(QQAdapter)

    from yukichan_bot.plugin_loader import load_enabled_plugins

    load_enabled_plugins()
    nonebot.run()


if __name__ == "__main__":
    main()
