import re
from typing import Optional

from nonebot import on_command, on_fullmatch, on_regex
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg, RegexMatched
from nonebot.permission import SUPERUSER, Permission

from .core import ChessService, ReplyResult

chess_service = ChessService()


async def _is_admin_or_superuser(bot: Bot, event: Event) -> bool:
    if await SUPERUSER(bot, event):
        return True
    sender = getattr(event, "sender", None)
    if sender:
        role = getattr(sender, "role", "")
        if role in ("admin", "owner"):
            return True
    member = getattr(event, "member", None)
    if member:
        roles = getattr(member, "roles", [])
        if any(r in ("2", "4", 2, 4, "admin", "owner") for r in roles):
            return True
    return False


def _get_sender_info(event: Event) -> tuple[int, str]:
    raw_id = event.get_user_id()
    user_id = int(raw_id) if raw_id.isdigit() else hash(raw_id) & 0x7FFFFFFF

    sender = getattr(event, "sender", None)
    author = getattr(event, "author", None)

    name = ""
    if sender:
        name = getattr(sender, "card", "") or getattr(sender, "nickname", "")
    elif author:
        name = getattr(author, "username", "")

    if not name:
        name = str(raw_id)

    return user_id, name


def _get_group_code(event: Event) -> str:
    group_id = getattr(event, "group_id", None)
    group_openid = getattr(event, "group_openid", None)
    if group_id:
        return str(group_id)
    if group_openid:
        return str(group_openid)
    return event.get_session_id()


async def _send_reply(matcher, bot: Bot, event: Event, result: Optional[ReplyResult]) -> None:
    if result is None:
        return

    adapter_name = bot.adapter.get_name()
    if adapter_name == "OneBot V11":
        from nonebot.adapters.onebot.v11 import Message, MessageSegment

        msg = Message()
        if result.at_user_id:
            msg += MessageSegment.at(result.at_user_id) + " "
        if result.text:
            msg += MessageSegment.text(result.text)
        if result.image_bytes:
            msg += MessageSegment.image(result.image_bytes)
        await matcher.finish(msg)
    elif adapter_name == "QQ":
        from nonebot.adapters.qq import Message, MessageSegment

        msg = Message()
        if result.at_user_id:
            msg += MessageSegment.mention_user(str(result.at_user_id)) + " "
        if result.text:
            msg += MessageSegment.text(result.text)
        if result.image_bytes:
            msg += MessageSegment.file_image(result.image_bytes)
        await matcher.finish(msg)
    else:
        text = result.text
        if result.at_user_id:
            text = f"@{result.at_user_id} {text}"
        await matcher.finish(text)


# Matchers
game_matcher = on_fullmatch(["下棋", "chess"], priority=2, block=True)


@game_matcher.handle()
async def _(bot: Bot, event: Event):
    user_id, name = _get_sender_info(event)
    group_code = _get_group_code(event)
    res = chess_service.game(group_code, user_id, name)
    await _send_reply(game_matcher, bot, event, res)


blind_matcher = on_fullmatch(["盲棋", "blind"], priority=2, block=True)


@blind_matcher.handle()
async def _(bot: Bot, event: Event):
    user_id, name = _get_sender_info(event)
    group_code = _get_group_code(event)
    res = chess_service.blindfold(group_code, user_id, name)
    await _send_reply(blind_matcher, bot, event, res)


resign_matcher = on_fullmatch(["认输", "resign"], priority=2, block=True)


@resign_matcher.handle()
async def _(bot: Bot, event: Event):
    user_id, _ = _get_sender_info(event)
    group_code = _get_group_code(event)
    res = chess_service.resign(group_code, user_id)
    await _send_reply(resign_matcher, bot, event, res)


draw_matcher = on_fullmatch(["和棋", "draw"], priority=2, block=True)


@draw_matcher.handle()
async def _(bot: Bot, event: Event):
    user_id, _ = _get_sender_info(event)
    group_code = _get_group_code(event)
    res = chess_service.draw(group_code, user_id)
    await _send_reply(draw_matcher, bot, event, res)


abort_matcher = on_fullmatch(
    ["中断", "abort"],
    permission=Permission(_is_admin_or_superuser),
    priority=2,
    block=True,
)


@abort_matcher.handle()
async def _(bot: Bot, event: Event):
    group_code = _get_group_code(event)
    res = chess_service.abort(group_code)
    await _send_reply(abort_matcher, bot, event, res)


play_matcher = on_regex(
    r"^[!|！]([0-8]|[R|N|B|Q|K|O|a-h|x]|[-|=|+])+$", priority=2, block=True
)


@play_matcher.handle()
async def _(bot: Bot, event: Event, matched: str = RegexMatched()):
    user_id, _ = _get_sender_info(event)
    group_code = _get_group_code(event)
    move_str = matched.replace("！", "!")[1:]
    res = chess_service.play(user_id, group_code, move_str)
    await _send_reply(play_matcher, bot, event, res)


ranking_matcher = on_fullmatch(["排行榜", "ranking"], priority=2, block=True)


@ranking_matcher.handle()
async def _(bot: Bot, event: Event):
    res = chess_service.ranking()
    await _send_reply(ranking_matcher, bot, event, res)


rate_matcher = on_fullmatch(["等级分", "rate"], priority=2, block=True)


@rate_matcher.handle()
async def _(bot: Bot, event: Event):
    user_id, name = _get_sender_info(event)
    res = chess_service.rate(user_id, name)
    await _send_reply(rate_matcher, bot, event, res)


clean_rate_matcher = on_command(
    "clean.rate",
    aliases={".clean.rate", "清空等级分"},
    permission=SUPERUSER,
    priority=2,
    block=True,
)


@clean_rate_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    target_str = arg.extract_plain_text().strip()
    if target_str.isdigit():
        res = chess_service.clean_user_rate(int(target_str))
    else:
        res = ReplyResult(text=f"解析失败「{target_str}」不是正确的 QQ 号。")
    await _send_reply(clean_rate_matcher, bot, event, res)


pgn2gif_matcher = on_command("pgn2gif", priority=2, block=True)


@pgn2gif_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    pgn_str = arg.extract_plain_text().strip()
    pattern = r"([0-9]|[R|N|B|Q|K|O|a-h|x]|[-|.|=|+|#|/| |\n])+"
    if re.fullmatch(pattern, pgn_str):
        res = chess_service.generate_gif(pgn_str)
        await _send_reply(pgn2gif_matcher, bot, event, res)


lichess_matcher = on_regex(
    r"^https://lichess\.org/([0-9]|[a-z]|[A-Z])+$", priority=2, block=True
)


@lichess_matcher.handle()
async def _(bot: Bot, event: Event):
    url = event.get_plaintext().strip()
    res = await chess_service.parse_lichess_link(url)
    await _send_reply(lichess_matcher, bot, event, res)


cheese_matcher = on_fullmatch("cheese", priority=2, block=True)


@cheese_matcher.handle()
async def _(bot: Bot, event: Event):
    res = chess_service.cheese()
    await _send_reply(cheese_matcher, bot, event, res)


help_matcher = on_fullmatch(["帮助", "help"], priority=2, block=True)


@help_matcher.handle()
async def _(bot: Bot, event: Event):
    res = chess_service.get_help()
    await _send_reply(help_matcher, bot, event, res)
