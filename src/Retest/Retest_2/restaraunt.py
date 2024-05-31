import time
from dataclasses import dataclass
from queue import Queue
from random import choice, randint
from typing import Dict, List, Optional, Tuple


@dataclass
class Dish:
    name: str
    price: int
    cooking_time: int


@dataclass
class HotDish(Dish):
    dish_type: str = "hot_dish"


@dataclass
class ColdDish(Dish):
    dish_type: str = "cold_dish"


class Table:
    def __init__(self) -> None:
        self.ready_dishes: List[ColdDish | HotDish] = []
        self.cooked_dishes: List[ColdDish | HotDish] = []

    def do_order(self, menu: Dict[str, List[ColdDish | HotDish]]) -> List[ColdDish | HotDish]:
        wanted_dish: List[ColdDish | HotDish] = []
        hot, cold = menu["hot_dish"], menu["cold_dish"]
        wanted_dish += hot[randint(0, len(hot) // 2) : randint(len(hot) // 2, len(hot))]
        wanted_dish += cold[randint(0, len(cold) // 2) : randint(len(cold) // 2, len(cold))]
        return wanted_dish

    def get_table_money(self) -> int:
        money = sum([dish.price for dish in self.ready_dishes])
        return money

    def give_tips(self, waiter: "Waiter") -> None:
        waiter.salary += randint(0, 100)


class Waiter:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.salary: int = 0
        self.tables: Dict[int, Table] = {}
        self.restaurant_cash = 0

    def take_order(self, table_id: int, menu: Dict[str, List[ColdDish | HotDish]]) ->  List[ColdDish | HotDish]:
        order = self.tables[table_id].do_order(menu)
        self.tables[table_id].cooked_dishes = order
        return order

    def end_order(self, table_id: int) -> None:
        table_money = self.tables[table_id].get_table_money()
        self.restaurant_cash += table_money


class Kitchen:
    def __init__(self, section: str) -> None:
        self.section = section
        self.hot_order: Dict[int, List[ColdDish | HotDish]] = {}
        self.cold_order: Dict[int, List[ColdDish | HotDish]] = {}

    def add_order(
        self,
        table_id: int,
        order: list[ColdDish | HotDish],
    ) -> None:
        for dish in order:

            if dish.dish_type == "hot_dish":
                if table_id in self.hot_order:
                    self.hot_order[table_id].append(dish)
                else:
                    self.hot_order[table_id] = [dish]
            elif dish.dish_type == "cold_dish":
                if table_id in self.cold_order:
                    self.cold_order[table_id].append(dish)
                else:
                    self.cold_order[table_id] = [dish]
            else:
                raise ValueError("Unknown dish")

    def cooking_hot_dish(self) -> Optional[ColdDish | HotDish]:
        if len(self.hot_order) == 0 or self.hot_order.items() == []:
            return None
        table_id = choice(list(self.hot_order.keys()))
        dish_num = randint(0, len(self.hot_order[table_id]) - 1)
        result = self.hot_order[table_id][dish_num]
        del self.hot_order[table_id][dish_num]
        if len(self.hot_order[table_id]) == 0:
            del self.hot_order[table_id]
        # time.sleep(0.1)  # cooking
        return result

    def cooking_cold_dish(self) -> Optional[ColdDish | HotDish]:
        if len(self.cold_order) == 0:
            return None
        table_id = choice(list(self.cold_order.keys()))
        dish_num = randint(0, len(self.cold_order[table_id]) - 1)
        result = self.cold_order[table_id][dish_num]
        del self.cold_order[table_id][dish_num]
        if len(self.cold_order[table_id]) == 0:
            del self.cold_order[table_id]
        # time.sleep(0.1)  # cooking
        return result


class Restaurant:
    def __init__(self, name: str):
        self.name: str = name
        self.menu: Dict[str, List[ColdDish | HotDish]] = {"hot_dish": [], "cold_dish": []}
        self.tables: Dict[int, Table] = {}
        self.free_tables: Queue[int] = Queue()
        self.waiters: List[Waiter] = []
        self.free_waiters: Queue[Waiter] = Queue()
        self.kitchen = Kitchen(f"Kitchen of {self.name}")

    def add_dish(self, name: str, price: int, cooking_time: int, dish_type: str) -> None:
        if dish_type == 'cold_dish':
            dish: ColdDish|HotDish = ColdDish(name, price, cooking_time, dish_type)
        else:
            dish = HotDish(name, price, cooking_time, dish_type)
        if dish in self.menu[dish.dish_type]:
            raise KeyError("That dish already exist")
        self.menu[dish.dish_type].append(dish)

    def add_waiter(self, name: str) -> None:
        self.waiters.append(Waiter(name))
        self.free_waiters.put(self.waiters[-1])

    def add_table(self, table_id: int) -> None:
        if table_id in self.tables:
            raise KeyError("Such table is already exist")
        self.tables[table_id] = Table()
        self.free_tables.put(table_id)

    def get_menu_list(self) -> str:
        menu_list = ""
        for dish in self.menu:
            menu_list += f"{self.menu[dish]}"
        return menu_list

    def accept_table(self) -> int:
        if self.free_tables.empty() or self.free_waiters.empty():
            raise Exception("Restaurant if full")
        free_tabel_id = self.free_tables.get()
        free_waiter = self.free_waiters.get()
        free_waiter.tables[free_tabel_id] = self.tables[free_tabel_id]

        order = free_waiter.take_order(free_tabel_id, self.menu)
        self.kitchen.add_order(free_tabel_id, order)
        dish = self.kitchen.cooking_hot_dish()
        while dish is not None:
            free_waiter.tables[free_tabel_id].ready_dishes.append(dish)
            dish = self.kitchen.cooking_hot_dish()
        dish = self.kitchen.cooking_cold_dish()
        while dish is not None:
            free_waiter.tables[free_tabel_id].ready_dishes.append(dish)
            dish = self.kitchen.cooking_cold_dish()

        free_waiter.end_order(free_tabel_id)
        free_waiter.tables[free_tabel_id].give_tips(free_waiter)
        money = free_waiter.restaurant_cash
        del free_waiter.tables[free_tabel_id]
        self.free_waiters.put(free_waiter)
        self.free_tables.put(free_tabel_id)
        return money
