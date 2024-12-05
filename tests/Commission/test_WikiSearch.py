import pytest

from src.Commission.WikiSearch.PagesFinder import PageNode, get_path_to_page, get_random_page


def test_get_random_page():
    page = get_random_page()
    assert isinstance(page, PageNode) and page.url is not None


@pytest.mark.parametrize(
    "page, path",
    (
        (PageNode("A", PageNode("B", PageNode("C", None))), ["C", "B", "A"]),
        (PageNode("X", PageNode("Y", None)), ["Y", "X"]),
        (PageNode("Hitler", None), ["Hitler"]),
    ),
)
def test_get_path_to_page(page, path):
    assert get_path_to_page(page) == path
