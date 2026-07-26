import datetime
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

import chess
import chess.pgn
import httpx

from .db import DBService
from .elo import calculate_new_rate
from .render import (
    generate_board_png_bytes,
    generate_gif_bytes_from_pgn,
)

ASSETS_DIR = Path(__file__).parent / "assets"


def _is_april_fools_day() -> bool:
    now = datetime.datetime.now()
    return now.month == 4 and now.day == 1


@dataclass
class ChessRoom:
    board: chess.Board = field(default_factory=chess.Board)
    white_player: int = 0
    white_name: str = ""
    black_player: int = 0
    black_name: str = ""
    draw_player: int = 0
    last_move_time: float = field(default_factory=time.time)
    is_blindfold: bool = False
    white_err: bool = False
    black_err: bool = False


@dataclass
class ReplyResult:
    text: str
    image_bytes: Optional[bytes] = None
    at_user_id: Optional[Union[int, str]] = None


class ChessService:
    def __init__(self, db_service: Optional[DBService] = None) -> None:
        self.game_rooms: dict[Union[int, str], ChessRoom] = {}
        self.db_service = db_service or DBService()

    def get_chess_string(self, room: ChessRoom) -> str:
        site_str = '[Site "github.com/aimerneige/yukichan-bot"]\n'
        date_str = f'[Date "{datetime.datetime.now().strftime("%Y-%m-%d")}"]\n'
        white_str = f'[White "{room.white_name}"]\n'
        black_str = f'[Black "{room.black_name}"]\n'

        game = chess.pgn.Game()
        node = game
        temp_board = chess.Board()
        for move in room.board.move_stack:
            node = node.add_variation(move)
            temp_board.push(move)

        exporter = chess.pgn.StringExporter(
            headers=False, comments=False, variations=False
        )
        moves_str = game.accept(exporter)

        return site_str + date_str + white_str + black_str + moves_str

    def _get_elo_string(
        self, room: ChessRoom, white_score: float, black_score: float
    ) -> str:
        if room.white_player == 0 or room.black_player == 0:
            return ""

        white_rate = (
            self.db_service.get_elo_rate_by_uin(room.white_player) or 500
        )
        black_rate = (
            self.db_service.get_elo_rate_by_uin(room.black_player) or 500
        )

        new_white, new_black = calculate_new_rate(
            white_rate, black_rate, white_score, black_score
        )

        self.db_service.update_elo_by_uin(
            room.white_player, room.white_name, new_white
        )
        self.db_service.update_elo_by_uin(
            room.black_player, room.black_name, new_black
        )

        return f"玩家等级分：\n{room.white_name}：{new_white}\n{room.black_name}：{new_black}\n\n"

    def game(
        self, group_code: Union[int, str], sender_uin: int, sender_name: str
    ) -> ReplyResult:
        return self._create_game(False, group_code, sender_uin, sender_name)

    def blindfold(
        self, group_code: Union[int, str], sender_uin: int, sender_name: str
    ) -> ReplyResult:
        return self._create_game(True, group_code, sender_uin, sender_name)

    def _create_game(
        self,
        is_blindfold: bool,
        group_code: Union[int, str],
        sender_uin: int,
        sender_name: str,
    ) -> ReplyResult:
        if group_code in self.game_rooms:
            room = self.game_rooms[group_code]
            if room.black_player != 0:
                if (time.time() - room.last_move_time) > 21600:
                    abort_res = self.abort(group_code)
                    abort_res.text = (
                        "对局已存在超过 6 小时，游戏结束。\n\n"
                        "已有对局已被中断，如需创建新对局请重新发送指令。"
                    )
                    abort_res.at_user_id = sender_uin
                    return abort_res

                msg = (
                    "对局已在进行中，无法创建或加入对局，当前对局玩家为："
                    f"@{room.white_name} @{room.black_name}，"
                    "群主或管理员发送「中断」或「abort」可中断对局（自动判和）。"
                )
                return ReplyResult(text=msg, at_user_id=sender_uin)

            if sender_uin == room.white_player:
                return ReplyResult(
                    text="请等候其他玩家加入游戏。", at_user_id=sender_uin
                )

            if room.is_blindfold and not is_blindfold:
                return ReplyResult(
                    text="已创建盲棋对局，请加入或等待盲棋对局结束之后创建普通对局。"
                )
            if not room.is_blindfold and is_blindfold:
                return ReplyResult(
                    text="已创建普通对局，请加入或等待普通对局结束之后创建盲棋对局。"
                )

            room.black_player = sender_uin
            room.black_name = sender_name
            room.last_move_time = time.time()

            if is_blindfold:
                return ReplyResult(
                    text="黑棋已加入对局，请白方下棋。",
                    at_user_id=room.white_player,
                )

            png_bytes = generate_board_png_bytes(room.board)
            return ReplyResult(
                text="黑棋已加入对局，请白方下棋。",
                image_bytes=png_bytes,
                at_user_id=room.white_player,
            )

        self.game_rooms[group_code] = ChessRoom(
            board=chess.Board(),
            white_player=sender_uin,
            white_name=sender_name,
            is_blindfold=is_blindfold,
            last_move_time=time.time(),
        )

        if is_blindfold:
            return ReplyResult(
                text="已创建新的盲棋对局，发送「盲棋」或「blind」可加入对局。"
            )
        return ReplyResult(
            text="已创建新的对局，发送「下棋」或「chess」可加入对局。"
        )

    def abort(self, group_code: Union[int, str]) -> ReplyResult:
        if group_code not in self.game_rooms:
            return ReplyResult(
                text="对局不存在，发送「下棋」或「chess」可创建对局。"
            )

        room = self.game_rooms.pop(group_code)
        chess_string = self.get_chess_string(room)

        if len(room.board.move_stack) > 4:
            self.db_service.create_pgn(
                chess_string,
                room.white_player,
                room.black_player,
                room.white_name,
                room.black_name,
            )

        return ReplyResult(
            text=f"对局已被管理员中断，游戏结束。\n\n{chess_string}"
        )

    def draw(
        self, group_code: Union[int, str], sender_uin: int
    ) -> ReplyResult:
        if group_code not in self.game_rooms:
            return ReplyResult(
                text="对局不存在，发送「下棋」或「chess」可创建对局。"
            )

        room = self.game_rooms[group_code]
        if sender_uin not in (room.white_player, room.black_player):
            return ReplyResult(
                text="不是对局中的玩家，无法请求和棋。", at_user_id=sender_uin
            )

        room.last_move_time = time.time()
        if room.draw_player == 0:
            room.draw_player = sender_uin
            return ReplyResult(
                text="请求和棋，发送「和棋」或「draw」接受和棋。走棋视为拒绝和棋。",
                at_user_id=sender_uin,
            )
        if room.draw_player == sender_uin:
            return ReplyResult(
                text="已发起和棋请求，请勿重复发送。", at_user_id=sender_uin
            )

        # Accept draw
        self.game_rooms.pop(group_code)
        chess_string = self.get_chess_string(room)
        elo_string = ""

        if len(room.board.move_stack) > 4:
            self.db_service.create_pgn(
                chess_string,
                room.white_player,
                room.black_player,
                room.white_name,
                room.black_name,
            )
            elo_string = self._get_elo_string(room, 0.5, 0.5)

        gif_bytes = generate_gif_bytes_from_pgn(chess_string)
        return ReplyResult(
            text=f"接受和棋，游戏结束。\n{elo_string}{chess_string}",
            image_bytes=gif_bytes,
            at_user_id=sender_uin,
        )

    def resign(
        self, group_code: Union[int, str], sender_uin: int
    ) -> ReplyResult:
        if group_code not in self.game_rooms:
            return ReplyResult(
                text="对局不存在，发送「下棋」或「chess」可创建对局。"
            )

        room = self.game_rooms[group_code]
        if sender_uin not in (room.white_player, room.black_player):
            return ReplyResult(
                text="不是对局中的玩家，无法认输。", at_user_id=sender_uin
            )

        if room.white_player == 0 or room.black_player == 0:
            self.game_rooms.pop(group_code)
            return ReplyResult(text="对局已释放。")

        resign_color = (
            chess.WHITE if sender_uin == room.white_player else chess.BLACK
        )
        april_fools = _is_april_fools_day()

        if april_fools:
            resign_color = not resign_color

        self.game_rooms.pop(group_code)
        chess_string = self.get_chess_string(room)
        elo_string = ""

        if len(room.board.move_stack) > 4:
            self.db_service.create_pgn(
                chess_string,
                room.white_player,
                room.black_player,
                room.white_name,
                room.black_name,
            )
            white_score = 0.0 if resign_color == chess.WHITE else 1.0
            black_score = 1.0 - white_score
            elo_string = self._get_elo_string(room, white_score, black_score)

        gif_bytes = generate_gif_bytes_from_pgn(chess_string)

        if april_fools:
            text = f"对手认输，游戏结束，你胜利了。\n{elo_string}{chess_string}"
        else:
            text = f"认输，游戏结束。\n{elo_string}{chess_string}"

        return ReplyResult(
            text=text, image_bytes=gif_bytes, at_user_id=sender_uin
        )

    def play(
        self, sender_uin: int, group_code: Union[int, str], move_str: str
    ) -> Optional[ReplyResult]:
        if group_code not in self.game_rooms:
            return ReplyResult(
                text="对局不存在，发送「下棋」或「chess」可创建对局。",
                at_user_id=sender_uin,
            )

        room = self.game_rooms[group_code]

        if (
            sender_uin not in (room.white_player, room.black_player)
            and not _is_april_fools_day()
        ):
            return None

        if room.white_player == 0 or room.black_player == 0:
            return ReplyResult(
                text="请等候其他玩家加入游戏。", at_user_id=sender_uin
            )

        current_turn = room.board.turn
        current_player = (
            room.white_player if current_turn == chess.WHITE else room.black_player
        )

        if sender_uin != current_player and not _is_april_fools_day():
            return ReplyResult(text="请等待对手走棋。", at_user_id=sender_uin)

        room.last_move_time = time.time()

        # Attempt move
        parsed_move: Optional[chess.Move] = None
        try:
            parsed_move = room.board.parse_san(move_str)
        except ValueError:
            try:
                parsed_move = room.board.parse_uci(move_str)
            except ValueError:
                parsed_move = None

        if parsed_move is None or parsed_move not in room.board.legal_moves:
            if not room.is_blindfold:
                return ReplyResult(
                    text=f"移动「{move_str}」违规，请检查，格式请参考「代数记谱法」(Algebraic notation)。"
                )

            # Blindfold rules
            if sender_uin == room.white_player:
                if not room.white_err:
                    room.white_err = True
                    return ReplyResult(
                        text=f"移动「{move_str}」违例，再次违例会立即判负。"
                    )
            else:
                if not room.black_err:
                    room.black_err = True
                    return ReplyResult(
                        text=f"移动「{move_str}」违例，再次违例会立即判负。"
                    )

            # Second violation -> forfeit game
            self.game_rooms.pop(group_code)
            chess_string = self.get_chess_string(room)
            gif_bytes = generate_gif_bytes_from_pgn(chess_string)
            return ReplyResult(
                text=f"违例两次，游戏结束。\n{chess_string}",
                image_bytes=gif_bytes,
                at_user_id=sender_uin,
            )

        # Execute move
        last_move_uci = parsed_move.uci()
        room.board.push(parsed_move)

        if room.draw_player != 0:
            room.draw_player = 0

        # Check game over
        if room.board.is_game_over():
            self.game_rooms.pop(group_code)
            outcome = room.board.outcome()
            white_score, black_score = 0.5, 0.5
            msg = "游戏结束，"

            if outcome and outcome.winner is not None:
                if outcome.winner == chess.WHITE:
                    white_score, black_score = 1.0, 0.0
                    winner = "白方"
                else:
                    white_score, black_score = 0.0, 1.0
                    winner = "黑方"
                msg += f"{winner}胜利，因为将杀。\n"
            else:
                if room.board.is_fivefold_repetition():
                    msg += "和棋，因为五次重复走子。\n"
                elif room.board.is_seventyfive_moves():
                    msg += "和棋，因为七十五步规则。\n"
                elif room.board.is_insufficient_material():
                    msg += "和棋，因为不可能将死。\n"
                elif room.board.is_stalemate():
                    msg += "和棋，因为逼和（无子可动和棋）。\n"
                else:
                    msg += "和棋。\n"

            chess_string = self.get_chess_string(room)
            elo_string = ""

            if len(room.board.move_stack) > 4:
                self.db_service.create_pgn(
                    chess_string,
                    room.white_player,
                    room.black_player,
                    room.white_name,
                    room.black_name,
                )
                elo_string = self._get_elo_string(
                    room, white_score, black_score
                )

            gif_bytes = generate_gif_bytes_from_pgn(chess_string)
            return ReplyResult(
                text=f"{msg}{elo_string}{chess_string}",
                image_bytes=gif_bytes,
            )

        # Game continues
        next_player = (
            room.white_player
            if room.board.turn == chess.WHITE
            else room.black_player
        )
        if room.is_blindfold:
            return ReplyResult(
                text="对手已走子，游戏继续。", at_user_id=next_player
            )

        png_bytes = generate_board_png_bytes(
            room.board, last_move_uci=last_move_uci
        )
        return ReplyResult(
            text="对手已走子，游戏继续。",
            image_bytes=png_bytes,
            at_user_id=next_player,
        )

    def ranking(self) -> ReplyResult:
        highest_list = self.db_service.get_highest_rate_list()
        ret = "当前等级分排行榜：\n\n"
        for item in highest_list:
            ret += f"{item['name']}: {item['rate']}\n"
        return ReplyResult(text=ret)

    def rate(self, sender_uin: int, sender_name: str) -> ReplyResult:
        rate = self.db_service.get_elo_rate_by_uin(sender_uin)
        if rate is None:
            return ReplyResult(
                text="没有查找到等级分信息。请至少进行一局对局。"
            )
        return ReplyResult(text=f"玩家「{sender_name}」目前的等级分：{rate}")

    def clean_user_rate(self, target_uin: int) -> ReplyResult:
        success = self.db_service.clean_elo_by_uin(target_uin)
        if not success:
            return ReplyResult(
                text="没有查找到等级分信息。请检查用户 uid 是否正确。"
            )
        return ReplyResult(text=f"已清空用户「{target_uin}」的等级分。")

    def generate_gif(self, pgn_str: str) -> ReplyResult:
        try:
            gif_bytes = generate_gif_bytes_from_pgn(pgn_str)
            return ReplyResult(text="", image_bytes=gif_bytes)
        except Exception as e:
            return ReplyResult(text=f"GIF 生成失败，错误信息：{e}")

    async def parse_lichess_link(self, url: str) -> Optional[ReplyResult]:
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            if res.status_code != 200:
                return None
            html = res.text
            matched = re.search(r'<div class="pgn">([\S\s]*?)</div>', html)
            if not matched:
                return None
            pgn = matched.group(1).replace("&quot;", '"')
            return self.generate_gif(pgn)

    def cheese(self) -> ReplyResult:
        cheese_path = ASSETS_DIR / "cheese.jpeg"
        image_bytes = cheese_path.read_bytes() if cheese_path.exists() else None
        return ReplyResult(
            text="Chess Cheese Cheese Chess", image_bytes=image_bytes
        )

    def get_help(self) -> ReplyResult:
        help_path = ASSETS_DIR / "help.txt"
        text = (
            help_path.read_text(encoding="utf-8")
            if help_path.exists()
            else "暂无帮助信息"
        )
        return ReplyResult(text=text)
