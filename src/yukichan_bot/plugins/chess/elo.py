import math


def get_k_factor(rate_a: int, rate_b: int) -> int:
    if rate_a > 2400 and rate_b > 2400:
        return 16
    if rate_a > 2100 and rate_b > 2100:
        return 24
    return 32


def calculate_exception(rate: int, opponent_rate: int) -> float:
    return 1.0 / (1.0 + math.pow(10.0, float(opponent_rate - rate) / 400.0))


def calculate_rate(rate: int, score: float, exception: float, k: int) -> int:
    new_rate = round(float(rate) + float(k) * (score - exception))
    if new_rate < 1:
        new_rate = 1
    return new_rate


def calculate_new_rate(
    white_rate: int, black_rate: int, white_score: float, black_score: float
) -> tuple[int, int]:
    k = get_k_factor(white_rate, black_rate)
    exception_white = calculate_exception(white_rate, black_rate)
    exception_black = calculate_exception(black_rate, white_rate)
    new_white = calculate_rate(white_rate, white_score, exception_white, k)
    new_black = calculate_rate(black_rate, black_score, exception_black, k)
    return new_white, new_black
