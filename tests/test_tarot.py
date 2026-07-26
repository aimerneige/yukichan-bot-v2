from yukichan_bot.plugins.tarot.core import draw_cards, get_tarot_help, rotate_180
from yukichan_bot.plugins.tarot.meanings import format_card_meaning, get_card_info
from PIL import Image
import io


def test_tarot_help():
    text, img_bytes = get_tarot_help()
    assert "运势预测" in text
    assert len(img_bytes) > 0


def test_draw_cards_with_meanings():
    cards_1 = draw_cards(1)
    assert len(cards_1) == 1
    assert len(cards_1[0].image_bytes) > 0
    assert "【" in cards_1[0].meaning_text
    assert "关键词：" in cards_1[0].meaning_text
    assert "解析：" in cards_1[0].meaning_text

    cards_3 = draw_cards(3)
    assert len(cards_3) == 3


def test_meanings_formatting():
    info_0 = get_card_info(0)
    assert info_0["name"] == "愚者 (The Fool)"

    text_upright = format_card_meaning("00_Fool", is_upright=True)
    assert "正位" in text_upright
    assert "愚者" in text_upright

    text_reversed = format_card_meaning("00_Fool", is_upright=False)
    assert "逆位" in text_reversed


def test_rotate_180():
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    original_bytes = buf.getvalue()

    rotated_bytes = rotate_180(original_bytes)
    assert len(rotated_bytes) > 0
