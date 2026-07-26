from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from .core import (
    check_ytdlp_installed,
    cleanup_file,
    download_video,
    get_video_info,
)

ytdlp_matcher = on_command(
    "yt-dlp", aliases={"/yt-dlp"}, permission=SUPERUSER, priority=6, block=True
)


@ytdlp_matcher.handle()
async def _(bot: Bot, event: Event, arg=CommandArg()):
    url = arg.extract_plain_text().strip()
    if not url:
        return

    if not check_ytdlp_installed():
        await ytdlp_matcher.finish("目标服务器未安装 yt-dlp。")

    title, size_str, err = await get_video_info(url)
    if err:
        await ytdlp_matcher.finish(err)

    await ytdlp_matcher.send(
        f"视频标题：{title}\n视频大小：{size_str}\n即将开始下载视频，请稍候。"
    )

    user_id = event.get_user_id()
    file_path, dl_err = await download_video(url, user_id)
    if dl_err or not file_path:
        await ytdlp_matcher.finish(dl_err or "视频下载失败。")

    await ytdlp_matcher.send("文件下载成功，正在上传，请稍候。")

    adapter_name = bot.adapter.get_name()
    try:
        if adapter_name == "OneBot V11":
            from nonebot.adapters.onebot.v11 import MessageSegment

            # If sending via video segment
            await ytdlp_matcher.finish(
                MessageSegment.video(f"file://{file_path.resolve()}")
            )
        elif adapter_name == "QQ":
            from nonebot.adapters.qq import MessageSegment

            if hasattr(MessageSegment, "file_video"):
                await ytdlp_matcher.finish(
                    MessageSegment.file_video(file_path.read_bytes())
                )
            else:
                await ytdlp_matcher.finish(
                    f"视频下载完成，保存路径: {file_path.name}"
                )
        else:
            await ytdlp_matcher.finish(
                f"视频下载完成，已保存至本地: {file_path.name}"
            )
    finally:
        cleanup_file(file_path)
