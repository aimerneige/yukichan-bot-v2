import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.adapters.qq import Adapter as QQAdapter


def main() -> None:
    nonebot.init(driver="~fastapi+~httpx+~websockets")

    driver = nonebot.get_driver()
    driver.register_adapter(OneBotV11Adapter)
    driver.register_adapter(QQAdapter)

    from yukichan_bot.plugin_loader import load_enabled_plugins

    load_enabled_plugins()
    nonebot.run()


if __name__ == "__main__":
    main()
