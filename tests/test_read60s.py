import pytest
from yukichan_bot.plugins.read60s.core import fetch_60s_news


@pytest.mark.anyio
async def test_fetch_60s_news(httpx_mock=None):
    # Tests that function runs without unhandled crash
    img_bytes, err_msg = await fetch_60s_news()
    assert (img_bytes is not None and err_msg == "") or (
        img_bytes is None and len(err_msg) > 0
    )
