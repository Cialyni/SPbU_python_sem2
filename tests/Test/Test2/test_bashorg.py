import pytest

from src.Tests.test2.bashorg import *


@pytest.mark.parametrize("quote_num", (10, 5, 11))
def test_get_best_quote(quote_num) -> None:
    quote_lst = get_best_quote(quote_num)
    assert len(quote_lst) == quote_num
    for quote in quote_lst:
        assert isinstance(quote, str)



@pytest.mark.parametrize("quote_num", (10, 5, 111))
def test_get_random_quote(quote_num) -> None:
    quote_lst = get_random_quote(quote_num)
    assert len(quote_lst) == quote_num
    for quote in quote_lst:
        assert isinstance(quote, str)


@pytest.mark.parametrize("quote_num", (10, 5, 111))
def test_get_last_quote(quote_num) -> None:
    quote_lst = get_last_quote(quote_num)
    assert len(quote_lst) == quote_num
    for quote in quote_lst:
        assert isinstance(quote, str)