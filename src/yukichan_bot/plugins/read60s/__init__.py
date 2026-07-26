from nonebot import on_fullmatch
from nonebot.adapters import Bot, Event

from .core import fetch_60s_news

read60s_matcher = on_fullmatch(["今日新闻", "早报", "60s"], priority=7, block=True)


@read60s_matcher.handle()
async def _(bot: Bot, event: Event):
    img_bytes, err_msg = await fetch_60s_news()
    if err_msg or not img_bytes:
        await read60s_matcher.finish(err_msg or "获取早报失败。")

    adapter_name = bot.adapter.get_name()

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import MessageSegment

        await read60s_matcher.finish(MessageSegment.image(img_bytes))
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import MessageSegment

        await read60s_matcher.finish(MessageSegment.file_image(img_bytes))
    else:
        await read60s_matcher.finish("[早报图片已获取，但当前平台无法展示]")
