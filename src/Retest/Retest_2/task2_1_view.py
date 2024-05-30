from random import choice
from tkinter import *
from typing import List


class MainWindom(Tk):
    def __init__(self, n: int, buttons, f):
        super().__init__()
        self.n = n
        self.build_window(buttons, f)

    def build_window(self, buttons, f):
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
                buttons[i * self.n + j] = Button(
                    Frm, text=" ", command=lambda a=i * self.n + j: f(buttons_values[a], buttons[a], a)
                )
                buttons[i * self.n + j].pack(side=LEFT, expand=YES, fill=BOTH)


class WinWindow(Tk):
    def __init__(self):
        super().__init__()
        self.build_win_window()

    def build_win_window(self):
        self.geometry("250x200")
        self.title("WINWINWIN")
        label = Label(self, text="WIN")
        label.pack(anchor=CENTER, expand=1)
