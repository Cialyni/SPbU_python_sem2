import pytest

from src.Retest.Retest_2.restaraunt import *

rest = Restaurant("mac_kfs")


def test_add_dishes():
    for lst in (
        ["rise", 32, 15, "hot_dish"],
        ["grechka", 20, 15, "hot_dish"],
        ["Chicken", 605, 100, "hot_dish"],
        ["IceCream", 100, 1, "cold_dish"],
    ):
        rest.add_dish(*lst)
    assert "cold_dish" in rest.menu
    assert "hot_dish" in rest.menu


def test_add_tables():
    for i in range(10):
        rest.add_table(i)
    assert len(rest.tables) == 10


def test_add_waiter():
    for name in ["a1", "b3", "r2"]:
        rest.add_waiter(name)
    assert len(rest.waiters) == 3


def test_acceptance_of_table():

    assert rest.accept_table() != 0
