from yukichan_bot.plugins.fadian.core import get_fadian_post, get_fadian_text


def test_get_fadian_post_default():
    res = get_fadian_post()
    assert isinstance(res, str)
    assert len(res) > 0
    assert "解析 JSON 失败" not in res
    assert "阿咪" not in res


def test_get_fadian_post_custom_name():
    res = get_fadian_post("小明")
    assert isinstance(res, str)
    assert len(res) > 0
    assert "小明" in res or "解析 JSON 失败" not in res


def test_get_fadian_text():
    res = get_fadian_text()
    assert isinstance(res, str)
    assert len(res) > 0
    assert "解析 JSON 失败" not in res
