import time


def string_hash(s: str) -> int:
    h = 2166136261
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h


def get_fortune_result(hash_val: int) -> str:
    key = hash_val % 100
    if key < 2:
        return "上吉"
    elif key < 10:
        return "大吉"
    elif key < 38:
        return "上上"
    elif key < 42:
        return "上中"
    elif key < 45:
        return "上平"
    elif key < 46:
        return "上"
    elif key < 49:
        return "中吉"
    elif key < 51:
        return "中上"
    elif key < 57:
        return "中中"
    elif key < 66:
        return "中平"
    elif key < 71:
        return "中"
    elif key < 72:
        return "平中"
    elif key < 73:
        return "平平"
    elif key < 74:
        return "平"
    elif key < 99:
        return "下"
    elif key < 100:
        return "下下"
    else:
        return "大凶"


def draw_a_fortune_stick(things: str, uin: int) -> str:
    unix_time = (int(time.time()) // 10000) & 0xFFFFFFFF
    things_hash = string_hash(things)
    uin_hash = string_hash(str(uin))
    total_hash = (unix_time + things_hash + uin_hash) & 0xFFFFFFFF
    return get_fortune_result(total_hash)
