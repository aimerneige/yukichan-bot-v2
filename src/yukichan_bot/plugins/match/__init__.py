from nonebot import on_message
from nonebot.adapters import Event
from nonebot.rule import Rule

MATCH_RULES: dict[str, str] = {
    "老婆": "肥宅不要乱叫老婆啊！",
}


def is_matched_message(event: Event) -> bool:
    return event.get_plaintext() in MATCH_RULES


match_matcher = on_message(rule=Rule(is_matched_message), priority=10, block=True)


@match_matcher.handle()
async def reply_to_matched_message(event: Event) -> None:
    text = event.get_plaintext()
    if text in MATCH_RULES:
        await match_matcher.finish(MATCH_RULES[text])
