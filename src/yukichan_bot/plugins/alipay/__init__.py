from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg

from .core import fetch_alipay_voice

alipay_matcher = on_command("支付宝到账", aliases={"alipay"}, priority=8, block=True)


@alipay_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    amount_str = arg.extract_plain_text().strip()
    if not amount_str:
        return

    audio_bytes, err_msg = await fetch_alipay_voice(amount_str)
    if err_msg or not audio_bytes:
        await alipay_matcher.finish(err_msg or "语音生成失败。")

    adapter_name = bot.adapter.get_name()
    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import MessageSegment

        await alipay_matcher.finish(MessageSegment.record(audio_bytes))
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import MessageSegment

        if hasattr(MessageSegment, "file_audio"):
            await alipay_matcher.finish(MessageSegment.file_audio(audio_bytes))
        else:
            await alipay_matcher.finish("当前平台暂不支持语音消息。")
    else:
        await alipay_matcher.finish("[支付宝到账语音处理成功]")
