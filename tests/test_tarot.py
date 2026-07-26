from yukichan_bot.plugins.tarot.core import draw_cards, get_tarot_help, rotate_180
from PIL import Image
import io


def test_tarot_help():
    text, img_bytes = get_tarot_help()
    assert "运势预测" in text
    assert len(img_bytes) > 0


def test_draw_cards():
    cards_1 = draw_cards(1)
    assert len(cards_1) == 1
    assert len(cards_1[0]) > 0

    cards_3 = draw_cards(3)
    assert len(cards_3) == 3

    cards_invalid = draw_cards(10)
    assert len(cards_invalid) == 1


def test_rotate_180():
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    original_bytes = buf.getvalue()

    rotated_bytes = rotate_180(original_bytes)
    assert len(rotated_bytes) > 0
