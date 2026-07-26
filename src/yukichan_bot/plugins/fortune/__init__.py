from nonebot import on_command
from nonebot.adapters import Event
from nonebot.params import CommandArg

from .core import draw_a_fortune_stick

fortune_matcher = on_command("求签", priority=6, block=True)


@fortune_matcher.handle()
async def _(event: Event, arg=CommandArg()):
    things = arg.extract_plain_text().strip()
    if not things:
        return

    user_id_str = event.get_user_id()
    try:
        uin = int(user_id_str)
    except ValueError:
        uin = hash(user_id_str) & 0xFFFFFFFF

    result = draw_a_fortune_stick(things, uin)
    await fortune_matcher.finish(f'所求事项"{things}"的求签结果为: {result}')
