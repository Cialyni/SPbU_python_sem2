from random import choice

import pytest

from src.Commission.TickTackToe.model import *

MODEL = GameModel()


class TestPlayer:
    pl1 = Human("A", choice("XO"))
    pl2 = EasyBot("B", choice("XO"))
    pl3 = HardBot("C", choice("XO"))
    MODEL.clear()

    def test_move_human(self):
        move = TestPlayer.pl1.move(MODEL.available_fields, MODEL.board, choice(MODEL.available_fields))
        assert move not in MODEL.available_fields and MODEL.board[move] == TestPlayer.pl1.side

    def test_move_easy_bot(self):
        move = TestPlayer.pl2.move(MODEL.available_fields, MODEL.board, None)
        assert move not in MODEL.available_fields and MODEL.board[move] == TestPlayer.pl2.side

    def test_move_hard_bot(self):
        move = TestPlayer.pl3.move(MODEL.available_fields, MODEL.board, None)
        assert move not in MODEL.available_fields and MODEL.board[move] == TestPlayer.pl3.side


class TestModel:
    @pytest.mark.parametrize(
        "player, field_pos",
        (
            (Human("A", "X"), 4),
            (Human("B", "O"), 7),
            (EasyBot("C", "X"), None),
            (EasyBot("D", "O"), None),
            (HardBot("E", "X"), None),
            (HardBot("F", "O"), None),
        ),
    )
    def test_make_move(self, player, field_pos):
        move = MODEL.make_move(player, field_pos)
        assert move not in MODEL.available_fields
        assert MODEL.board[move] == player.side

    def test_clear(self):
        MODEL.clear()
        flag = True
        for field in MODEL.board:
            if field != "":
                flag = False
        assert len(MODEL.available_fields) == 9 and flag
