import pytest

from src.Test.Test_1.task_1 import Magazine, Basket, Product

M = Magazine()
M.product_list = [
    Product(name="carrot", price=100, rating=0.8, count=5),
    Product(name="onion", price=913, rating=43, count=54),
    Product(name="cucumber", price=1000, rating=40, count=5111),
    Product(name="cabbage", price=76, rating=8, count=23),
]


@pytest.mark.parametrize(
    "type_sorting, expected",
    (
        (
            "rating",
            [
                Product(name="carrot", price=100, rating=0.8, count=5),
                Product(name="cabbage", price=76, rating=8, count=23),
                Product(name="cucumber", price=1000, rating=40, count=5111),
                Product(name="onion", price=913, rating=43, count=54),
            ],
        ),
        (
            "price",
            [
                Product(name="cabbage", price=76, rating=8, count=23),
                Product(name="carrot", price=100, rating=0.8, count=5),
                Product(name="onion", price=913, rating=43, count=54),
                Product(name="cucumber", price=1000, rating=40, count=5111),
            ],
        ),
        (
            "count",
            [
                Product(name="carrot", price=100, rating=0.8, count=5),
                Product(name="cabbage", price=76, rating=8, count=23),
                Product(name="onion", price=913, rating=43, count=54),
                Product(name="cucumber", price=1000, rating=40, count=5111),
            ],
        ),
        (
            "name",
            [
                Product(name="cabbage", price=76, rating=8, count=23),
                Product(name="carrot", price=100, rating=0.8, count=5),
                Product(name="cucumber", price=1000, rating=40, count=5111),
                Product(name="onion", price=913, rating=43, count=54),
            ],
        ),
    ),
)
def test_sorting(expected, type_sorting):
    assert M.sorting(type_sorting) == expected


@pytest.mark.parametrize(
    "expected, name",
    (
        (Product(name="carrot", price=100, rating=0.8, count=5), "carrot"),
        (Product(name="cucumber", price=1000, rating=40, count=5111), "cucumber"),
    ),
)
def test_find_product(expected, name):
    assert M.find_product(name) == expected
