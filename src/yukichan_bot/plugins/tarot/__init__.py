from nonebot import on_command, on_fullmatch
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg

from .core import DrawnCard, draw_cards, get_tarot_help

tarot_help_matcher = on_fullmatch(["塔罗", "塔罗牌", "tarot"], priority=7, block=True)


async def _send_drawn_cards(
    matcher, bot: Bot, cards: list[DrawnCard], header_text: str = ""
) -> None:
    if not cards:
        await matcher.finish("未能成功抽取塔罗牌，请稍后重试。")

    meaning_lines = []
    if header_text:
        meaning_lines.append(header_text)

    for i, card in enumerate(cards, 1):
        if len(cards) > 1:
            meaning_lines.append(f"第 {i} 张：{card.meaning_text}")
        else:
            meaning_lines.append(card.meaning_text)

    full_text = "\n\n".join(meaning_lines)

    adapter_name = bot.adapter.get_name()
    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = Message()
        if full_text:
            msg += MessageSegment.text(full_text + "\n")
        for card in cards:
            if card.image_bytes:
                msg += MessageSegment.image(card.image_bytes)
        await matcher.finish(msg)

    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = Message()
        if full_text:
            msg += MessageSegment.text(full_text + "\n")
        for card in cards:
            if card.image_bytes:
                msg += MessageSegment.file_image(card.image_bytes)
        await matcher.finish(msg)

    else:
        await matcher.finish(full_text)


@tarot_help_matcher.handle()
async def _(bot: Bot, event: Event):
    text, img = get_tarot_help()
    adapter_name = bot.adapter.get_name()

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = Message(text)
        if img:
            msg += MessageSegment.image(img)
        await tarot_help_matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = Message(text)
        if img:
            msg += MessageSegment.file_image(img)
        await tarot_help_matcher.finish(msg)
    else:
        await tarot_help_matcher.finish(text)


predict_matcher = on_fullmatch("运势预测", priority=7, block=True)


@predict_matcher.handle()
async def _(bot: Bot, event: Event):
    cards = draw_cards(1)
    await _send_drawn_cards(predict_matcher, bot, cards, header_text="【每日运势预测】")


divine_matcher = on_fullmatch("塔罗占卜", priority=7, block=True)


@divine_matcher.handle()
async def _(bot: Bot, event: Event):
    cards = draw_cards(3)
    await _send_drawn_cards(divine_matcher, bot, cards, header_text="【塔罗占卜结果】")


draw_matcher = on_command("抽塔罗牌", priority=7, block=True)


@draw_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    count_str = arg.extract_plain_text().strip()
    if not count_str:
        return

    try:
        count = int(count_str)
    except ValueError:
        await draw_matcher.finish("牌数解析失败")

    if count <= 0 or count > 8:
        count = 1

    cards = draw_cards(count)
    await _send_drawn_cards(
        draw_matcher, bot, cards, header_text=f"【抽取 {len(cards)} 张塔罗牌】"
    )
