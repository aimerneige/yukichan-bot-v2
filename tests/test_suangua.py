from yukichan_bot.plugins.suangua.core import cal_hash, get_suangua_message


def test_cal_hash():
    h1 = cal_hash("财运", 10001)
    h2 = cal_hash("财运", 10001)
    assert 1 <= h1 <= 64
    assert h1 == h2


def test_get_suangua_message_zero():
    explain, img_bytes = get_suangua_message(0)
    assert "算卦不算命" in explain
    assert img_bytes is not None
    assert len(img_bytes) > 0


def test_get_suangua_message_valid():
    explain, img_bytes = get_suangua_message(1)
    assert "第1卦" in explain
    assert img_bytes is not None
    assert len(img_bytes) > 0
