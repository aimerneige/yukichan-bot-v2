import asyncio
import shutil
import time
from pathlib import Path

TEMP_DIR = Path("data/temp/ytdlp")


def check_ytdlp_installed() -> bool:
    return shutil.which("yt-dlp") is not None


async def get_video_info(url: str) -> tuple[str, str, str]:
    if not check_ytdlp_installed():
        return "", "", "目标服务器未安装 yt-dlp。"

    try:
        proc_title = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--print",
            "%(title)s",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out_title, err_title = await proc_title.communicate()

        if proc_title.returncode != 0:
            return (
                "",
                "",
                "获取视频标题失败，可能是服务器无法访问该链接或链接失效。",
            )

        title = out_title.decode("utf-8", errors="replace").strip()

        proc_size = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--print",
            "%(filesize,filesize_approx)s",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out_size, err_size = await proc_size.communicate()
        size_str = out_size.decode("utf-8", errors="replace").strip()

        return title, size_str, ""
    except Exception as e:
        return "", "", f"解析视频元数据发生异常: {e}"


async def download_video(url: str, sender_id: str) -> tuple[Path | None, str]:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{sender_id}_{int(time.time())}.mp4"
    output_path = TEMP_DIR / filename

    try:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            url,
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "-o",
            str(output_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0 and output_path.exists():
            return output_path, ""
        else:
            err_log = stderr.decode("utf-8", errors="replace").strip()
            return None, f"视频文件下载失败:\n{err_log[:200]}"
    except Exception as e:
        return None, f"下载视频发生异常: {e}"


def cleanup_file(path: Path | None) -> None:
    if path and path.exists():
        try:
            path.unlink()
        except Exception:
            pass
