import abc
from tkinter import Tk, ttk
from typing import Any, Dict, Optional

from src.Commission.TickTackToe.model import EasyBot, GameException, GameModel, HardBot, Human, Session
from src.Commission.TickTackToe.view import ChoseSideView, EndView, GameView, MainView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: GameModel) -> None:
        self.model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, model: GameModel, root: Tk) -> None:
        self.model = model
        self.root = root

        self.viewmodels: dict[str, IViewModel] = {
            "main": MainViewModel(self.model),
            "game": GameViewModel(self.model),
            "chose": ChoseSideViewModel(self.model),
            "end": EndViewModel(self.model),
        }
        self._session_callback_rm = model.add_session_listener(self._session_observer)
        self.current_view: Optional[ttk.Frame] = None

    def _session_observer(self, session: Session) -> None:
        if session is None:
            self.switch("main", {})
        elif session.view_type == "game":
            self.switch("game", {})
        elif session.view_type == "chose":
            self.switch("chose", {})
        elif session.view_type == "end_game":
            self.switch("end", {})
        elif session.view_type == "menu":
            self.switch("main", {})

    def switch(self, name: str, data: dict) -> None:
        if name not in self.viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self.current_view is not None:
            self.current_view.destroy()
        self.current_view = self.viewmodels[name].start(self.root, data)
        self.current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("main", {})


class MainViewModel(IViewModel):
    def _bind(self, view: MainView) -> None:
        view.play_button_easy.config(command=lambda: self.play_with_easy_bot())
        view.play_button_hard.config(command=lambda: self.play_with_hard_bot())
        view.play_button_friend.config(command=lambda: self.play_with_friend())

    def play_with_easy_bot(self) -> None:
        self.model.change_session("chose", [Human("Player", ""), EasyBot("Easy Bot", "")])

    def play_with_hard_bot(self) -> None:
        self.model.change_session("chose", [Human("Player", ""), HardBot("Hard Bot", "")])

    def play_with_friend(self) -> None:
        self.model.change_session("chose", [Human("Player1", ""), Human("Player2", "")])

    def start(self, root: Tk, data: Dict) -> ttk.Frame:
        frame = MainView(root)
        self._bind(frame)
        return frame


class ChoseSideViewModel(IViewModel):
    def _bind(self, view: ChoseSideView) -> None:
        view.x_button.config(command=lambda: self.play_with_x())
        view.o_button.config(command=lambda: self.play_with_o())

    def play_with_x(self) -> None:
        pl1, pl2 = self.model.get_enemies()
        pl1.side = "X"
        pl1.ready_for_move = True
        pl2.side = "O"
        pl2.ready_for_move = False
        self.model.change_session("game", self.model.get_enemies(), None)

    def play_with_o(self) -> None:
        pl1, pl2 = self.model.get_enemies()
        pl1.side = "O"
        pl1.ready_for_move = False
        pl2.side = "X"
        pl2.ready_for_move = True
        self.model.change_session("game", self.model.get_enemies(), None)

    def start(self, root: Tk, data: Dict) -> ttk.Frame:
        frame = ChoseSideView(root)
        self._bind(frame)
        return frame


class GameViewModel(IViewModel):

    def _bind(self, view: GameView) -> None:
        for i in range(9):
            cmd = lambda field=i: self.make_full_turn(view, field)
            view.buttons[i].config(command=cmd)  # avoiding mypy error

    def start_fist_turn(self, view: GameView) -> None:
        pl1, pl2 = self.model.get_enemies()
        cur_player = pl1 if pl1.ready_for_move else pl2
        if isinstance(cur_player, HardBot) or isinstance(cur_player, EasyBot):
            self.make_move(view, None)

    def make_move(self, view: GameView, field: Optional[int]) -> None:
        try:
            pl1, pl2 = self.model.get_enemies()
        except GameException:
            return
        cur_player = pl1 if pl1.ready_for_move else pl2
        move = self.model.make_move(cur_player, field)
        if move is not None:
            self.model.change_turn()
            view.buttons[move].config(text=cur_player.side)
            if self.model.check_win():
                self.model.change_session("end_game", None, f"{cur_player.name} WON")

            if self.model.check_draw():
                self.model.change_session("end_game", None, "DRAW")

    def make_full_turn(self, view: GameView, field_num: Optional[int]) -> None:

        pl1, pl2 = self.model.get_enemies()
        if isinstance(pl1, HardBot) or isinstance(pl1, EasyBot) or isinstance(pl2, HardBot) or isinstance(pl2, EasyBot):
            self.make_move(view, field_num)
        self.make_move(view, field_num)

    def start(self, root: Tk, data: Dict) -> ttk.Frame:
        frame = GameView(self.model.get_enemies()[1].name, root)
        self.start_fist_turn(frame)
        self._bind(frame)
        return frame


class EndViewModel(IViewModel):

    def _bind(self, view: EndView) -> None:
        view.menu_button.config(command=lambda: self.return_menu())

    def return_menu(self) -> None:
        self.model.clear()
        self.model.change_session("menu", None)

    def start(self, root: Tk, data: Dict) -> ttk.Frame:
        frame = EndView(self.model.session.value.winner if self.model.session.value else None, root)
        self._bind(frame)
        return frame
