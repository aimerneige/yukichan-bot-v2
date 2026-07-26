import nonebot

try:
    nonebot.get_driver()
except ValueError:
    nonebot.init(driver="~fastapi+~httpx+~websockets")

