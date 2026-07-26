import io
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image

from .meanings import format_card_meaning

ASSETS_DIR = Path(__file__).parent / "assets"


@dataclass
class DrawnCard:
    image_bytes: bytes
    card_filename: str
    is_upright: bool
    meaning_text: str


def rotate_180(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    rotated = img.rotate(180)
    buf = io.BytesIO()
    fmt = img.format if img.format else "PNG"
    rotated.save(buf, format=fmt)
    return buf.getvalue()


def draw_cards(number: int) -> list[DrawnCard]:
    if number <= 0 or number > 8:
        number = 1

    theme = "bilibili" if random.randint(0, 2) == 0 else "classic"
    deck_dir = ASSETS_DIR / "deck" / theme

    if not deck_dir.exists():
        return []

    card_files = [
        f
        for f in deck_dir.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]
    if not card_files:
        return []

    selected = random.sample(card_files, min(number, len(card_files)))
    result: list[DrawnCard] = []

    for card_path in selected:
        card_bytes = card_path.read_bytes()
        is_upright = random.randint(0, 1) == 1

        if not is_upright:
            try:
                card_bytes = rotate_180(card_bytes)
            except Exception:
                pass

        meaning_text = format_card_meaning(card_path.stem, is_upright)
        result.append(
            DrawnCard(
                image_bytes=card_bytes,
                card_filename=card_path.stem,
                is_upright=is_upright,
                meaning_text=meaning_text,
            )
        )

    return result


def get_tarot_help() -> tuple[str, bytes]:
    help_text = (
        "支持指令\n"
        "「运势预测」（单张牌预测运势）\n"
        "「塔罗占卜」（三张牌进行占卜）\n"
        "「抽塔罗牌 5」（抽取指定张数的塔罗牌）"
    )
    tarot_img_path = ASSETS_DIR / "tarot.jpg"
    img_bytes = (
        tarot_img_path.read_bytes() if tarot_img_path.exists() else b""
    )
    return help_text, img_bytes


# =====================================================================
# TODO: Mode B - AI Card Interpretation Mode (AI 智能解牌模式占位与预留)
# =====================================================================
# 预留配置项说明：
# - TAROT_INTERPRETATION_MODE: "fixed" | "ai" (默认 "fixed")
# - TAROT_AI_API_KEY: OpenAI / 大模型 API 密钥
# - TAROT_AI_BASE_URL: 大模型 API 地址 (默认 "https://api.openai.com/v1")
# - TAROT_AI_MODEL: 大模型名称 (如 "gpt-3.5-turbo", "gemini-1.5-flash")
# - TAROT_AI_DAILY_LIMIT_PER_USER: 单用户每日 AI 解牌限额 (默认 3 次/天)


async def get_ai_interpretation(
    cards: list[DrawnCard], user_id: int
) -> Optional[str]:
    """
    TODO: 接入大模型 (AI) 智能牌面解读功能 (含用户每日额度限制)

    实现步骤指南：
    1. 频次限额校验：查询 SQLite (如 tarot_ai_usage 表) 检查当前 user_id 今日已调用次数。
    2. 若超出 TAROT_AI_DAILY_LIMIT_PER_USER，返回 None（触发自动降级至 Mode A 固定的释义）。
    3. 构建 Prompt：将 cards 列表中的牌名与正/逆位拼接为专业占卜提示词。
    4. 异步请求：使用 httpx.AsyncClient() 发送 POST 请求至 TAROT_AI_BASE_URL/chat/completions。
    5. 记录配额：请求成功后更新 user_id 今日使用计数。
    6. 返回 AI 导出的解牌文本。
    """
    # 当前返回 None，默认自动使用 Mode A 固定释义模式
    return None
