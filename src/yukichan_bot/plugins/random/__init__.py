from nonebot import on_fullmatch
from nonebot.adapters import Bot, Event

from .core import draw_card, flip_coin, get_cxk_record, roll_dice

coin_matcher = on_fullmatch(["掷硬币", "/coin"], priority=6, block=True)
cxk_matcher = on_fullmatch("只因币", priority=6, block=True)
dice_matcher = on_fullmatch(["掷骰子", "/dice"], priority=6, block=True)
card_matcher = on_fullmatch(["抽扑克", "/card"], priority=6, block=True)


@coin_matcher.handle()
async def _(bot: Bot, event: Event):
    text = flip_coin()
    adapter_name = bot.adapter.get_name()
    user_id = event.get_user_id()

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = MessageSegment.at(user_id) + MessageSegment.text(" " + text)
        await coin_matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = MessageSegment.at(user_id) + MessageSegment.text(" " + text)
        await coin_matcher.finish(msg)
    else:
        await coin_matcher.finish(text)


@cxk_matcher.handle()
async def _(bot: Bot, event: Event):
    audio_bytes = get_cxk_record()
    if not audio_bytes:
        await cxk_matcher.finish("语音资源获取失败。")

    adapter_name = bot.adapter.get_name()
    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import MessageSegment

        await cxk_matcher.finish(MessageSegment.record(audio_bytes))
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import MessageSegment

        if hasattr(MessageSegment, "file_audio"):
            await cxk_matcher.finish(MessageSegment.file_audio(audio_bytes))
        else:
            await cxk_matcher.finish("当前平台暂不支持发送此语音片段。")
    else:
        await cxk_matcher.finish("无法在这个平台上发送语音。")


@dice_matcher.handle()
async def _(bot: Bot, event: Event):
    text = roll_dice()
    adapter_name = bot.adapter.get_name()
    user_id = event.get_user_id()

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import MessageSegment

        msg = MessageSegment.at(user_id) + MessageSegment.text(" " + text)
        await dice_matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import MessageSegment

        msg = MessageSegment.at(user_id) + MessageSegment.text(" " + text)
        await dice_matcher.finish(msg)
    else:
        await dice_matcher.finish(text)


@card_matcher.handle()
async def _(bot: Bot, event: Event):
    cards = draw_card(1)
    if not cards:
        await card_matcher.finish("发生错误，无法读取扑克图片")

    adapter_name = bot.adapter.get_name()
    img_bytes = cards[0]

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import MessageSegment

        await card_matcher.finish(MessageSegment.image(img_bytes))
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import MessageSegment

        await card_matcher.finish(MessageSegment.file_image(img_bytes))
    else:
        await card_matcher.finish("[ERROR] 读取图片失败或不支持此模式。")
