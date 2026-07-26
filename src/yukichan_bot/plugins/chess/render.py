import datetime
import io
from typing import Optional

import cairosvg
import chess
import chess.pgn
import chess.svg
from PIL import Image

GRAY_THEME = {
    "square light": "#F5F5F5",
    "square dark": "#BDBDBD",
    "square light lastmove": "#616161",
    "square dark lastmove": "#5C5C5C",
    "margin": "#212121",
    "coord": "#E2E2E2",
}

GREEN_THEME = {
    "square light": "#769656",
    "square dark": "#EEEED2",
    "square light lastmove": "#BACA2B",
    "square dark lastmove": "#F6F669",
    "margin": "#212121",
    "coord": "#E2E2E2",
}

RED_THEME = {
    "square light": "#f2cfb6",
    "square dark": "#c24539",
    "square light lastmove": "#e16b8c",
    "square dark lastmove": "#f06c91",
    "margin": "#212121",
    "coord": "#E2E2E2",
}


def _is_christmas_day(now: datetime.datetime) -> bool:
    return now.month == 12 and now.day == 25


def _is_new_year_day(now: datetime.datetime) -> bool:
    return now.month == 1 and now.day == 1


def _is_april_fools_day(now: datetime.datetime) -> bool:
    return now.month == 4 and now.day == 1


def _is_12_13_day(now: datetime.datetime) -> bool:
    return now.month == 12 and now.day == 13


def generate_board_svg(
    board: chess.Board,
    last_move_uci: Optional[str] = None,
    now: Optional[datetime.datetime] = None,
) -> str:
    if now is None:
        now = datetime.datetime.now()

    king_square = None
    if not _is_12_13_day(now) and board.is_check():
        king_square = board.king(board.turn)

    last_move = None
    if last_move_uci and last_move_uci != "None":
        try:
            last_move = chess.Move.from_uci(last_move_uci)
        except ValueError:
            last_move = None

    themes = None
    if _is_christmas_day(now) or _is_new_year_day(now):
        themes = RED_THEME
    elif _is_april_fools_day(now):
        themes = GREEN_THEME
    elif _is_12_13_day(now):
        themes = GRAY_THEME

    kwargs = {
        "board": board,
        "orientation": board.turn,
        "lastmove": last_move,
        "check": king_square,
        "size": 720,
        "coordinates": True,
    }
    if themes:
        kwargs["colors"] = themes

    return chess.svg.board(**kwargs)



def svg_to_png_bytes(svg_str: str) -> bytes:
    return cairosvg.svg2png(bytestring=svg_str.encode("utf-8"))


def generate_board_png_bytes(
    board: chess.Board,
    last_move_uci: Optional[str] = None,
    now: Optional[datetime.datetime] = None,
) -> bytes:
    svg_str = generate_board_svg(board, last_move_uci, now)
    return svg_to_png_bytes(svg_str)


def generate_gif_bytes_from_pgn(
    pgn_str: str, now: Optional[datetime.datetime] = None
) -> bytes:
    game = chess.pgn.read_game(io.StringIO(pgn_str))
    if game is None:
        raise ValueError("Invalid PGN string")

    board = game.board()
    images: list[Image.Image] = []

    # Initial position frame
    svg_str = generate_board_svg(board, last_move_uci=None, now=now)
    png_b = svg_to_png_bytes(svg_str)
    images.append(Image.open(io.BytesIO(png_b)).convert("RGBA"))

    for move in game.mainline_moves():
        board.push(move)
        svg_str = generate_board_svg(
            board, last_move_uci=move.uci(), now=now
        )
        png_b = svg_to_png_bytes(svg_str)
        images.append(Image.open(io.BytesIO(png_b)).convert("RGBA"))

    buf = io.BytesIO()
    if images:
        images[0].save(
            buf,
            format="GIF",
            save_all=True,
            append_images=images[1:],
            duration=1000,
            loop=0,
        )
    return buf.getvalue()
