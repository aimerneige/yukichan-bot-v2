from yukichan_bot.plugins.fortune.core import (
    draw_a_fortune_stick,
    get_fortune_result,
    string_hash,
)


def test_string_hash():
    # Test FNV-1a hash consistency
    assert string_hash("test") == string_hash("test")
    assert isinstance(string_hash("hello"), int)


def test_get_fortune_result():
    assert get_fortune_result(0) == "上吉"
    assert get_fortune_result(5) == "大吉"
    assert get_fortune_result(99) == "下下"


def test_draw_a_fortune_stick():
    res1 = draw_a_fortune_stick("考试", 123456)
    res2 = draw_a_fortune_stick("考试", 123456)
    assert res1 == res2
    assert isinstance(res1, str)
    assert len(res1) > 0
