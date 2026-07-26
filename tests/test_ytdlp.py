from pathlib import Path
from yukichan_bot.plugins.ytdlp.core import (
    check_ytdlp_installed,
    cleanup_file,
)


def test_check_ytdlp_installed():
    res = check_ytdlp_installed()
    assert isinstance(res, bool)


def test_cleanup_file(tmp_path: Path):
    test_file = tmp_path / "test_video.mp4"
    test_file.write_bytes(b"dummy video data")
    assert test_file.exists()

    cleanup_file(test_file)
    assert not test_file.exists()
