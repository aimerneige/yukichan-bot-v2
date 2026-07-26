import tempfile
from pathlib import Path

import pytest
from yukichan_bot.plugins.chess.db import DBService
from yukichan_bot.plugins.chess.elo import (
    calculate_exception,
    calculate_new_rate,
    calculate_rate,
    get_k_factor,
)
from yukichan_bot.plugins.chess.core import ChessService
from yukichan_bot.plugins.chess.render import (
    generate_board_png_bytes,
    generate_gif_bytes_from_pgn,
)


def test_elo_calculation():
    assert get_k_factor(2500, 2500) == 16
    assert get_k_factor(2200, 2200) == 24
    assert get_k_factor(1500, 1500) == 32

    exc_white = calculate_exception(1500, 1500)
    assert exc_white == pytest.approx(0.5)

    new_white, new_black = calculate_new_rate(1500, 1500, 1.0, 0.0)
    assert new_white == 1516
    assert new_black == 1484


def test_db_service():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_chess.db"
        db = DBService(db_path=str(db_path))

        assert db.get_elo_rate_by_uin(10001) is None

        db.create_elo(10001, "Alice", 1500)
        assert db.get_elo_rate_by_uin(10001) == 1500

        db.update_elo_by_uin(10001, "Alice", 1520)
        assert db.get_elo_rate_by_uin(10001) == 1520

        highest = db.get_highest_rate_list()
        assert len(highest) == 1
        assert highest[0]["name"] == "Alice"
        assert highest[0]["rate"] == 1520

        db.clean_elo_by_uin(10001)
        assert db.get_elo_rate_by_uin(10001) == 100

        db.create_pgn("1. e4 e5", 10001, 10002, "Alice", "Bob")


def test_chess_service_game_flow():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_chess.db"
        db = DBService(db_path=str(db_path))
        service = ChessService(db_service=db)

        # 1. White creates game
        res1 = service.game(group_code="group1", sender_uin=101, sender_name="WhitePlayer")
        assert "已创建新的对局" in res1.text

        # 2. Black joins game
        res2 = service.game(group_code="group1", sender_uin=102, sender_name="BlackPlayer")
        assert "黑棋已加入对局" in res2.text
        assert res2.image_bytes is not None

        # 3. White plays e4
        res3 = service.play(sender_uin=101, group_code="group1", move_str="e4")
        assert "对手已走子" in res3.text
        assert res3.image_bytes is not None

        # 4. Black plays e5
        res4 = service.play(sender_uin=102, group_code="group1", move_str="e5")
        assert "对手已走子" in res4.text

        # 5. Invalid move by White
        res_invalid = service.play(sender_uin=101, group_code="group1", move_str="invalid_move")
        assert "违规" in res_invalid.text

        # 6. Resign
        res_resign = service.resign(group_code="group1", sender_uin=102)
        assert "认输" in res_resign.text or "胜利" in res_resign.text
        assert res_resign.image_bytes is not None


def test_render_png_and_gif():
    import chess
    board = chess.Board()
    png_bytes = generate_board_png_bytes(board)
    assert png_bytes.startswith(b"\x89PNG")

    pgn_str = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"
    gif_bytes = generate_gif_bytes_from_pgn(pgn_str)
    assert gif_bytes.startswith(b"GIF89a") or gif_bytes.startswith(b"GIF87a")
