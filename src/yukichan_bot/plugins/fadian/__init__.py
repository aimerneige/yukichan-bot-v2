from nonebot import on_command, on_fullmatch
from nonebot.adapters import Event
from nonebot.params import CommandArg

from .core import get_fadian_post, get_fadian_text

fadian_post_matcher = on_command("每日发癫", priority=5, block=True)
fadian_text_matcher = on_fullmatch(["小作文", "发大病"], priority=6, block=True)


@fadian_post_matcher.handle()
async def _(event: Event, arg=CommandArg()):
    name_string = arg.extract_plain_text().strip()
    name = name_string if name_string else "小乌贼"
    await fadian_post_matcher.finish(get_fadian_post(name))


@fadian_text_matcher.handle()
async def _(event: Event):
    await fadian_text_matcher.finish(get_fadian_text())
