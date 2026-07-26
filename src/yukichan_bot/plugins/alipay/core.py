import httpx

API_URL_FMT = "https://mm.cqu.cc/share/zhifubaodaozhang/mp3/{}.mp3"


async def fetch_alipay_voice(amount_str: str) -> tuple[bytes | None, str]:
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "金额必须大于0。"
    except ValueError:
        return None, "金额格式不正确。"

    # Format amount if integer
    formatted_amount = (
        str(int(amount)) if amount.is_integer() else str(amount)
    )
    url = API_URL_FMT.format(formatted_amount)

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                return resp.content, ""
            return None, "获取支付宝音频失败，可能不支持该金额。"
        except Exception:
            return None, "网络错误，无法连接到语音服务器。"
