from nonebot import on_command, on_fullmatch
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg

from .core import draw_cards, get_tarot_help

tarot_help_matcher = on_fullmatch(["塔罗", "塔罗牌", "tarot"], priority=7, block=True)


async def _send_images(matcher, bot: Bot, images: list[bytes], text: str = "") -> None:
    adapter_name = bot.adapter.get_name()
    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = Message()
        if text:
            msg += MessageSegment.text(text)
        for img in images:
            if img:
                msg += MessageSegment.image(img)
        await matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = Message()
        if text:
            msg += MessageSegment.text(text)
        for img in images:
            if img:
                msg += MessageSegment.file_image(img)
        await matcher.finish(msg)
    else:
        await matcher.finish(text or f"抽到了 {len(images)} 张塔罗牌")


@tarot_help_matcher.handle()
async def _(bot: Bot, event: Event):
    text, img = get_tarot_help()
    await _send_images(tarot_help_matcher, bot, [img] if img else [], text=text)


predict_matcher = on_fullmatch("运势预测", priority=7, block=True)


@predict_matcher.handle()
async def _(bot: Bot, event: Event):
    cards = draw_cards(1)
    await _send_images(predict_matcher, bot, cards)


divine_matcher = on_fullmatch("塔罗占卜", priority=7, block=True)


@divine_matcher.handle()
async def _(bot: Bot, event: Event):
    cards = draw_cards(3)
    await _send_images(divine_matcher, bot, cards)


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
    await _send_images(draw_matcher, bot, cards)
