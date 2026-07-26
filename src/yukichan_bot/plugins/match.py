from nonebot import on_message
from nonebot.adapters import Event
from nonebot.rule import Rule


REPLY = "肥宅不要乱叫老婆啊！"


def is_wife_message(event: Event) -> bool:
    return event.get_plaintext() == "老婆"


wife_matcher = on_message(rule=Rule(is_wife_message), priority=10, block=True)


@wife_matcher.handle()
async def reply_to_wife_message() -> None:
    await wife_matcher.finish(REPLY)

