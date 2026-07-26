from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg

from .core import cal_hash, get_suangua_message

suangua_matcher = on_command("算卦", priority=6, block=True)


@suangua_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    things = arg.extract_plain_text().strip()
    result_index = 0
    if things:
        user_id_str = event.get_user_id()
        try:
            uin = int(user_id_str)
        except ValueError:
            uin = hash(user_id_str) & 0xFFFFFFFF
        result_index = cal_hash(things, uin)

    explain, img_bytes = get_suangua_message(result_index)
    if not img_bytes:
        await suangua_matcher.finish("发生了玄学事故！算卦失败了！")

    adapter_name = bot.adapter.get_name()

    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = Message()
        msg += MessageSegment.text(explain + "\n")
        msg += MessageSegment.image(img_bytes)
        await suangua_matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = Message()
        msg += MessageSegment.text(explain + "\n")
        msg += MessageSegment.file_image(img_bytes)
        await suangua_matcher.finish(msg)
    else:
        await suangua_matcher.finish(explain)
