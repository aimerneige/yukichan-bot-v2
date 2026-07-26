import random
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"


def flip_coin() -> str:
    if random.randint(0, 1) == 0:
        return "掷出了反面。"
    return "掷出了正面。"


def get_cxk_record() -> bytes | None:
    mp3_file = ASSETS_DIR / "cxk.mp3"
    if mp3_file.exists():
        return mp3_file.read_bytes()
    return None


def roll_dice() -> str:
    point = random.randint(1, 6)
    return f"掷出了 {point} 点。"


def draw_card(number: int = 1) -> list[bytes]:
    card_dir = ASSETS_DIR / "card"
    if not card_dir.exists():
        return []

    card_files = [
        f for f in card_dir.iterdir() if f.is_file() and not f.name.startswith(".")
    ]
    if not card_files:
        return []

    selected = random.sample(card_files, min(number, len(card_files)))
    return [f.read_bytes() for f in selected]
