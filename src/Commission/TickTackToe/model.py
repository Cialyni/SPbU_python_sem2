from dataclasses import dataclass
from random import choice
from typing import Any, Callable, List, Optional, Tuple

from loguru import logger

from src.Commission.TickTackToe.observer import Observable

wining_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class GameException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dataclass
class Session:
    view_type: str
    enemies: Optional[List["Player"]]
    winner: Optional[str]


class Player:
    def __init__(self, name: str, side: str) -> None:
        self.name = name
        self.side = side
        self.ready_for_move = True if self.side == "X" else False

    def move(self, available_moves: List[int], board: List[str], field: Optional[int]) -> Optional[int]:
        return field


class EasyBot(Player):
    def move(self, available_moves: List[int], board: List[str], field: Optional[int]) -> int:
        field = choice(available_moves)
        board[field] = self.side
        available_moves.pop(available_moves.index(field))
        return field


class HardBot(Player):

    def find_field_in_line(self, x_count: int, o_count: int, board: List[str]) -> Optional[int]:
        acceptable_move = []
        for line in wining_lines:
            x, o = 0, 0
            for i in range(3):
                if board[line[i]] == "X":
                    x += 1
                if board[line[i]] == "O":
                    o += 1
            if x == x_count and o == o_count:
                for i in range(3):
                    if board[line[i]] != "X" and board[line[i]] != "O":
                        acceptable_move.append(line[i])

        return choice(acceptable_move) if len(acceptable_move) != 0 else None

    def chose_field(self, available_moves: List[int], board: List[str]) -> int:
        if len(available_moves) == 9:  #  bot make first move
            return choice(available_moves)
        if len(available_moves) == 8:  # bot make second move
            if 4 in available_moves:
                return 4  # center
            else:
                return choice([0, 2, 6, 8])  # one of the corners
        step = None
        if self.side == "X":
            step = self.find_field_in_line(2, 0, board)
            if step is None:
                step = self.find_field_in_line(0, 2, board)
            if step is None:
                step = self.find_field_in_line(1, 0, board)
        else:
            step = self.find_field_in_line(0, 2, board)
            if step is None:
                step = self.find_field_in_line(2, 0, board)
            if step is None:
                step = self.find_field_in_line(0, 1, board)
        if step is not None:
            return step
        return choice(available_moves)

    def move(self, available_moves: List[int], board: List[str], field: Optional[int]) -> int:
        field = self.chose_field(available_moves, board)
        board[field] = self.side
        available_moves.pop(available_moves.index(field))
        return field


class Human(Player):
    def move(self, available_moves: List[int], board: List[str], field: Optional[int]) -> int:
        if field in available_moves:
            board[field] = self.side
            available_moves.pop(available_moves.index(field))
            return field
        raise GameException("Cant move like this")


class GameModel:
    def __init__(self) -> None:
        self.board = ["" for i in range(9)]
        self.available_fields = [i for i in range(9)]
        self.session: Observable = Observable()

    def make_move(self, player: Player, field_pos: Optional[int] = None) -> Optional[int]:
        try:
            return player.move(self.available_fields, self.board, field_pos)
        except GameException as e:
            logger.info(e)

    def check_win(self) -> bool:
        for line in wining_lines:
            if self.board[line[0]] != "" and self.board[line[0]] == self.board[line[1]] == self.board[line[2]]:
                return True
        return False

    def check_availability_of_move(self, field_num: int) -> bool:
        return field_num in self.available_fields

    def check_draw(self) -> bool:
        return len(self.available_fields) == 0

    def change_turn(self) -> None:
        pl1, pl2 = self.get_enemies()
        pl1.ready_for_move, pl2.ready_for_move = pl2.ready_for_move, pl1.ready_for_move

    def get_enemies(self) -> List[Player]:

        if self.session.value and self.session.value.enemies:
            return self.session.value.enemies
        raise GameException("Opponent not defined yet")

    def change_session(self, view_type: str, enemies: Optional[List[Player]], winner: Optional[str] = None) -> None:
        self.session.value = Session(view_type, enemies, winner)

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.session.add_callback(callback)

    def clear(self) -> None:
        self.board = ["" for i in range(9)]
        self.available_fields = [i for i in range(9)]
