import json
import random
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"
_post_data: list[str] = []
_text_data: list[str] = []


def _load_data() -> None:
    global _post_data, _text_data
    if not _post_data:
        post_file = ASSETS_DIR / "post.json"
        if post_file.exists():
            with open(post_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                _post_data = data.get("post", [])

    if not _text_data:
        text_file = ASSETS_DIR / "text.json"
        if text_file.exists():
            with open(text_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                _text_data = data.get("text", [])


def get_fadian_post(name: str = "小乌贼") -> str:
    _load_data()
    if not _post_data:
        return "解析 JSON 失败，请查阅后台日志。"
    template = random.choice(_post_data)
    return template.replace("阿咪", name)


def get_fadian_text() -> str:
    _load_data()
    if not _text_data:
        return "解析 JSON 失败，请查阅后台日志。"
    return random.choice(_text_data)
