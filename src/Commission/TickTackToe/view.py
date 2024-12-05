from tkinter import ttk
from typing import Any, Dict, Tuple


class MainView(ttk.Frame):
    GREETINGS = "Welcome to Tick Tack Toe!\n    Choose an opponent"
    PLAY_WITH_EASY_BOT = "Play with easy bot"
    PLAY_WITH_HARD_BOT = "Play with hard bot"
    PLAY_WITH_FRIEND = "Play with friend"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.greetings = ttk.Label(self, text=self.GREETINGS)
        self.greetings.grid(row=0, column=0, columnspan=2, padx=200, pady=50)
        self.play_button_easy = ttk.Button(self, text=self.PLAY_WITH_EASY_BOT)
        self.play_button_easy.grid(row=1, column=0, sticky="ew", padx=200, pady=10)
        self.play_button_hard = ttk.Button(self, text=self.PLAY_WITH_HARD_BOT)
        self.play_button_hard.grid(row=2, column=0, sticky="ew", padx=200, pady=10)
        self.play_button_friend = ttk.Button(self, text=self.PLAY_WITH_FRIEND)
        self.play_button_friend.grid(row=3, column=0, sticky="ew", padx=200, pady=10)


class EndView(ttk.Frame):
    RETURN_BUTTON_TEXT = "Return to menu"

    def __init__(self, winner_label: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.greetings = ttk.Label(self, text=winner_label)
        self.greetings.grid(row=0, column=0, columnspan=2, padx=200, pady=50)
        self.menu_button = ttk.Button(self, text=self.RETURN_BUTTON_TEXT)
        self.menu_button.grid(row=1, column=0, sticky="ew", padx=200, pady=10)


class GameView(ttk.Frame):

    def __init__(self, enemy: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.greetings = ttk.Label(self, text=f"Playing against {enemy}")
        self.greetings.grid(row=0, column=0, columnspan=4, padx=150, pady=50)
        self.buttons = []
        for i in range(1, 4):
            for j in range(1, 4):
                self.buttons.append(ttk.Button(self, text=""))
                self.buttons[-1].grid(row=i, column=j, sticky="nsew", padx=10, pady=10)


class ChoseSideView(ttk.Frame):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.chose_side = ttk.Label(self, text=f"Chose side")
        self.chose_side.grid(row=0, column=0, columnspan=4, padx=150, pady=50)
        self.x_button = ttk.Button(self, text="X")
        self.x_button.grid(row=1, column=0, sticky="ew", padx=200, pady=10)
        self.o_button = ttk.Button(self, text="O")
        self.o_button.grid(row=2, column=0, sticky="ew", padx=200, pady=10)
