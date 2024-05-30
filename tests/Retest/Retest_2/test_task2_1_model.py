from tkinter import *

import pytest

from src.Retest.Retest_2.task2_1_model import *

a = App(10)


def test_app_init():
    assert a.size == 10
    assert len(a.buttons) == 100
    assert issubclass(type(a.window), Tk)


def test_button_event_handler():
    a.button_event_handler(4, a.buttons[10], 10)
    assert a.active_button[-1] == [4, a.buttons[10], 10]
