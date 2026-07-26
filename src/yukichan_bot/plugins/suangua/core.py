import json
import time
from pathlib import Path
from typing import Tuple

ASSETS_DIR = Path(__file__).parent / "assets"
_gua_json_data: list[str] = []


def string_hash(s: str) -> int:
    h = 2166136261
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def cal_hash(things: str, uin: int) -> int:
    unix_time = (int(time.time()) // 10000) & 0xFFFFFFFF
    things_hash = string_hash(things)
    uin_hash = string_hash(str(uin))
    return ((unix_time + things_hash + uin_hash) % 64) + 1


def _load_data() -> None:
    global _gua_json_data
    if not _gua_json_data:
        json_file = ASSETS_DIR / "64.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                _gua_json_data = json.load(f)


def get_suangua_message(index: int) -> Tuple[str, bytes | None]:
    _load_data()
    if not _gua_json_data or index < 0 or index >= len(_gua_json_data):
        return "发生了玄学事故！算卦失败了！", None

    explain = _gua_json_data[index]
    img_path = ASSETS_DIR / "gua" / f"{index}.jpg"
    img_bytes = img_path.read_bytes() if img_path.exists() else None

    return explain, img_bytes
