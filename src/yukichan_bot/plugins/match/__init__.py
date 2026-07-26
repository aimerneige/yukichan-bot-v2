from nonebot import on_message
from nonebot.adapters import Event
from nonebot.rule import Rule

MATCH_RULES: dict[str, str] = {
    "老婆": "肥宅不要乱叫老婆啊！",
    "关于": (
        "ゆき酱国际象棋机器人\n"
        "本项目是使用 AGPL-3.0 开源协议授权的开源项目。\n"
        "开源地址及使用帮助：https://github.com/aimerneige/yukichan-bot-v2\n"
        "捐赠支持开发：https://aimer.aiursoft.cn/zh/donate/"
    ),
    "about": (
        "ゆき酱国际象棋机器人\n"
        "本项目是使用 AGPL-3.0 开源协议授权的开源项目。\n"
        "开源地址及使用帮助：https://github.com/aimerneige/yukichan-bot-v2\n"
        "捐赠支持开发：https://aimer.aiursoft.cn/zh/donate/"
    ),
}


def is_matched_message(event: Event) -> bool:
    return event.get_plaintext() in MATCH_RULES


match_matcher = on_message(rule=Rule(is_matched_message), priority=10, block=True)


@match_matcher.handle()
async def reply_to_matched_message(event: Event) -> None:
    text = event.get_plaintext()
    if text in MATCH_RULES:
        await match_matcher.finish(MATCH_RULES[text])
