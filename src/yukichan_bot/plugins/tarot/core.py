import io
import random
from pathlib import Path

from PIL import Image

ASSETS_DIR = Path(__file__).parent / "assets"


def rotate_180(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    rotated = img.rotate(180)
    buf = io.BytesIO()
    fmt = img.format if img.format else "PNG"
    rotated.save(buf, format=fmt)
    return buf.getvalue()


def draw_cards(number: int) -> list[bytes]:
    if number <= 0 or number > 8:
        number = 1

    theme = "bilibili" if random.randint(0, 2) == 0 else "classic"
    deck_dir = ASSETS_DIR / "deck" / theme

    if not deck_dir.exists():
        return []

    card_files = [f for f in deck_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not card_files:
        return []

    selected = random.sample(card_files, min(number, len(card_files)))
    result: list[bytes] = []

    for card_path in selected:
        card_bytes = card_path.read_bytes()
        if random.randint(0, 1) == 0:
            try:
                card_bytes = rotate_180(card_bytes)
            except Exception:
                pass
        result.append(card_bytes)

    return result


def get_tarot_help() -> tuple[str, bytes]:
    help_text = (
        "支持指令\n"
        "「运势预测」（单张牌预测运势）\n"
        "「塔罗占卜」（三张牌进行占卜）\n"
        "「抽塔罗牌 5」（抽取指定张数的塔罗牌）"
    )
    tarot_img_path = ASSETS_DIR / "tarot.jpg"
    img_bytes = tarot_img_path.read_bytes() if tarot_img_path.exists() else b""
    return help_text, img_bytes
