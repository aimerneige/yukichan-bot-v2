from yukichan_bot.plugins.random.core import (
    draw_card,
    flip_coin,
    get_cxk_record,
    roll_dice,
)


def test_flip_coin():
    res = flip_coin()
    assert res in ["掷出了正面。", "掷出了反面。"]


def test_get_cxk_record():
    data = get_cxk_record()
    assert data is not None
    assert len(data) > 0


def test_roll_dice():
    res = roll_dice()
    assert res.startswith("掷出了 ") and res.endswith(" 点。")


def test_draw_card():
    cards = draw_card(1)
    assert len(cards) == 1
    assert len(cards[0]) > 0
