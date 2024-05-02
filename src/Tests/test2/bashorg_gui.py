import asyncio
import tkinter.scrolledtext as scrolled_text
from tkinter import *

from bashorg import *
from config import *


class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.text_block_best = scrolled_text.ScrolledText(
            self, width=textblock_size[0], height=textblock_size[1], wrap="word", bg="LavenderBlush"
        )
        self.text_block_last = scrolled_text.ScrolledText(
            self, width=textblock_size[0], height=textblock_size[1], wrap="word", bg="LavenderBlush"
        )
        self.text_block_random = scrolled_text.ScrolledText(
            self, width=textblock_size[0], height=textblock_size[1], wrap="word", bg="LavenderBlush"
        )
        self.entry_best = Text(self, width=entry_n_size[0], height=entry_n_size[1], wrap="word", bg="peru")
        self.entry_last = Text(self, width=entry_n_size[0], height=entry_n_size[1], wrap="word", bg="peru")
        self.entry_random = Text(self, width=entry_n_size[0], height=entry_n_size[1], wrap="word", bg="peru")
        """task1 = asyncio.create_task(self.best_output)
        task2 = asyncio.create_task(self.best_output)
        task3 = asyncio.create_task(self.best_output)"""
        self.button_best = Button(self, text="Получить N лучших цитат", command=self.best_output, bg="grey70")
        self.button_last = Button(self, text="Получить N последних цитат", command=self.last_output, bg="grey70")
        self.button_random = Button(self, text="Получить N случайных цитат", command=self.random_output, bg="grey70")

    def packing(self) -> None:
        self.configure(
            bg="lightgreen",
        )
        self.resizable(width=False, height=False)
        w, h = screen_width, screen_height
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("BASHORG MEMES HERE")

        self.text_block_best.place(x=textblock_x, y=textblock_y[0])
        self.text_block_best.configure(state="disabled")
        self.text_block_last.place(x=textblock_x, y=textblock_y[0] + textblock_y[1])
        self.text_block_last.configure(state="disabled")
        self.text_block_random.place(x=textblock_x, y=textblock_y[0] + 2 * textblock_y[1])
        self.text_block_random.configure(state="disabled")

        self.entry_best.insert(1.0, "N = 10")
        self.entry_best.pack()
        self.entry_best.place(x=entry_n_x, y=entry_n_y[0])
        self.entry_last.insert(1.0, "N = 10")
        self.entry_last.pack()
        self.entry_last.place(x=entry_n_x, y=entry_n_y[0] + entry_n_y[1])
        self.entry_random.insert(1.0, "N = 10")
        self.entry_random.pack()
        self.entry_random.place(x=entry_n_x, y=entry_n_y[0] + 2 * entry_n_y[1])

        self.button_best.pack()
        self.button_best.configure(height=button_size[1], width=button_size[0])
        self.button_best.place(x=w // 2, y=button_y[0], anchor=CENTER)

        self.button_last.pack()
        self.button_last.configure(height=button_size[1], width=button_size[0])
        self.button_last.place(x=w // 2, y=button_y[0] + button_y[1], anchor=CENTER)

        self.button_random.pack()
        self.button_random.configure(height=button_size[1], width=button_size[0])
        self.button_random.place(x=w // 2, y=button_y[0] + 2 * button_y[1], anchor=CENTER)

    def random_output(self) -> None:
        self.text_block_random.configure(state=NORMAL)
        self.text_block_random.delete(1.0, END)
        string = self.entry_random.get(1.0, "end-1c")
        n = int(string.split()[2])
        text_lst = get_random_quote(n)[::-1]  # long
        for quote in text_lst:
            self.text_block_random.insert(1.0, quote + "\n")
        self.text_block_random.configure(state=DISABLED)

    def last_output(self) -> None:
        self.text_block_last.configure(state=NORMAL)
        self.text_block_last.delete(1.0, END)
        string = self.entry_last.get(1.0, "end-1c")
        n = int(string.split()[2])
        text_lst = get_last_quote(n)[::-1]  # long
        for quote in text_lst:
            self.text_block_last.insert(1.0, quote + "\n")
        self.text_block_last.configure(state=DISABLED)

    def best_output(self) -> None:
        self.text_block_best.configure(state=NORMAL)
        self.text_block_best.delete(1.0, END)
        string = self.entry_best.get(1.0, "end-1c")
        n = int(string.split()[2])
        text_lst = get_best_quote(n)[::-1]  # long
        for quote in text_lst:
            self.text_block_best.insert(1.0, quote + "\n")
        self.text_block_best.configure(state=DISABLED)


app = App()
app.packing()
app.mainloop()
