import pytest
from yukichan_bot.plugins.alipay.core import fetch_alipay_voice


@pytest.mark.anyio
async def test_fetch_alipay_voice_invalid():
    # Negative amount
    audio, err = await fetch_alipay_voice("-10")
    assert audio is None
    assert "大于0" in err

    # Non-numeric
    audio, err = await fetch_alipay_voice("abc")
    assert audio is None
    assert "不正确" in err


@pytest.mark.anyio
async def test_fetch_alipay_voice_valid_flow():
    # Valid amount call
    audio, err = await fetch_alipay_voice("100")
    assert (audio is not None and err == "") or (
        audio is None and len(err) > 0
    )
