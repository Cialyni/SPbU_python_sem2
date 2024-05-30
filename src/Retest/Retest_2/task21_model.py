import argparse
import time
from tkinter import DISABLED, Button, Tk
from typing import Dict, List

from src.Retest.Retest_2.task21_view import MainWindom, WinWindow


def args_pars() -> int:
    parser = argparse.ArgumentParser(description="Hitler game parameters")
    parser.add_argument(
        "N",
        type=int,
        help="an integer for the buttons count",
        nargs="?",
        default=2,
    )
    args = parser.parse_args()
    return args.N


class App:
    def __init__(self, n: int):
        self.size = n
        self.buttons: Dict[int, Button] = dict()
        self.count_of_unenable_button = 0
        self.active_button: List[List] = []
        self.window: MainWindom = MainWindom(n, self.buttons, self.button_event_handler)

    def run(self) -> None:
        while self.count_of_unenable_button != self.size**2:
            self.window.root.update()
        self.close()

    def close(self) -> None:
        self.closewindow = WinWindow()
        self.closewindow.root.update()
        time.sleep(1.5)

    def button_event_handler(self, button_num: int, btn: Button, ind: int) -> None:
        btn.configure(text=str(button_num))
        if len(self.active_button) != 0:
            if self.active_button[0][0] == button_num:
                self.count_of_unenable_button += 2
                self.buttons[ind]["state"] = DISABLED
                self.buttons[self.active_button[0][-1]]["state"] = DISABLED
                self.active_button.pop()
            else:

                self.buttons[self.active_button[0][-1]].configure(text="")
                self.active_button.pop()
                self.active_button.append([button_num, btn, ind])

        else:
            self.active_button.append([button_num, btn, ind])


if __name__ == "__main__":
    app = App(args_pars())
    app.run()
