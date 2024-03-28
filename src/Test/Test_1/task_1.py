from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    rating: float
    count: int = 0


class Basket:
    def __init__(self):
        self.products: [Product] = []

    def add_product(self, product: Product):
        self.products.append(product)

    def clear(self):
        self.products = []


class Magazine:
    def __init__(self):
        self.product_list: [Product] = []
        self.baskets = [Basket()]

    def add_new_product(self, name, price, rating, count):
        new_product = Product(name, price, rating, count)
        self.product_list.append(new_product)

    def find_product(self, name) -> Product | None:
        for elem in self.product_list:
            if elem.name == name:
                return elem
        return None

    def show_basket(self):
        for elem in self.baskets[-1].products:
            print(elem.name, elem.price, elem.rating, elem.count)

    def sorting(self, sort_type: str = "price"):
        if sort_type == "price":
            self.product_list = sorted(self.product_list, key=lambda x: x.price)
        if sort_type == "name":
            self.product_list = sorted(self.product_list, key=lambda x: x.name)
        if sort_type == "rating":
            self.product_list = sorted(self.product_list, key=lambda x: x.rating)
        if sort_type == "count":
            self.product_list = sorted(self.product_list, key=lambda x: x.count)
        return self.product_list

    def add_in_basket(self, name, price, rating, count):
        product = Product(name, price, rating, count)
        self.baskets[-1].add_product(product)

    def create_new_shopping_basket(self):
        self.baskets.append(Basket())

    def delete_active_basket(self):
        self.baskets.pop()

    def buy_active_basket(self) -> int:
        sum = 0
        for product in self.baskets[-1].products:
            market_product = self.find_product(product.name)
            if market_product is not None and market_product.count - product.count >= 0:
                self.product_list[self.product_list.index(market_product)].count -= product.count
                sum += product.count * product.price
            else:
                raise ValueError("In market no product or count of products less then needed:", product.name)
        self.baskets.pop()
        return sum


if __name__ == "__main__":
    magaz = Magazine()
    magaz.add_new_product("carrot", 100, 0.8, 5)
    magaz.add_new_product("onion", 913, 43, 54)
    magaz.add_new_product("cucumber", 1000, 40, 5111)
    magaz.add_new_product("cabbage", 76, 8, 23)
    print(magaz.sorting("rating"))
"""    magaz.add_in_basket("cucumber", 1000, 40, 5111)
    magaz.add_in_basket("carrot", 100, 0.8, 5)
    magaz.show_basket()"""

"""    print(magaz.buy_active_basket())"""
