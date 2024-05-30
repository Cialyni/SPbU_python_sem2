from random import choice
from tkinter import *
from typing import Callable, List

from mypyc.irbuild import function


class MainWindom:
    def __init__(self, n: int, buttons: dict, f: function) -> None:
        self.root = Tk()
        self.n: int = n
        self.build_window(buttons, f)

    def build_window(self, buttons: dict, f: function) -> None:
        defined_nums: List[int] = []
        buttons_values = dict()
        for i in range(self.n):
            Frm = Frame()
            Frm.pack(expand=YES, fill=BOTH)
            for j in range(self.n):
                buttons_values[i * self.n + j] = choice(
                    [i for i in range(0, self.n * self.n // 2) if defined_nums.count(i) < 2]
                )
                defined_nums.append(buttons_values[i * self.n + j])
                foo: Callable = lambda a=i * self.n + j: f(buttons_values[a], buttons[a], a)
                buttons[i * self.n + j] = Button(Frm, text=" ", command=foo)
                buttons[i * self.n + j].pack(side=LEFT, expand=YES, fill=BOTH)


class WinWindow:
    def __init__(self) -> None:
        self.root = Tk()
        self.build_win_window()

    def build_win_window(self) -> None:
        self.root.geometry("250x200")
        self.root.title("WINWINWIN")
        label = Label(self.root, text="WIN")
        label.pack(anchor=CENTER, expand=1)
