from typing import Tuple

import httpx

API_URL = "https://api.2xb.cn/zaob"


async def fetch_60s_news() -> Tuple[bytes | None, str]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(API_URL)
            if resp.status_code != 200:
                return None, "网络错误，获取早报信息失败。"
            data = resp.json()
        except Exception:
            return None, "网络错误，获取早报信息失败。"

        if data.get("msg") == "Success":
            image_url = data.get("imageUrl")
            if not image_url:
                return None, "API 错误，未找到早报图片地址。"
            try:
                img_resp = await client.get(image_url)
                if img_resp.status_code == 200:
                    return img_resp.content, ""
                return None, "网络错误，早报图片获取失败。"
            except Exception:
                return None, "网络错误，早报图片获取失败。"
        else:
            return None, "API 错误，无法获取早报图片。"
