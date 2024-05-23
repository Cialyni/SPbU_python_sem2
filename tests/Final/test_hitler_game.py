import pytest

from src.Final.hitler_page_finder import *


@pytest.mark.parametrize(
    "path",
    [
        [
            "https://en.wikipedia.org/wiki/President_of_Germany_(1919–1945)",
            "https://en.wikipedia.org/wiki/Adolf_Hitler",
        ]
    ],
)
def test_bfs_with_threads(path):
    assert bfs_with_threads(path[0], 5, 5) == path


def test_no_path():
    assert bfs_with_threads(["https://en.wikipedia.org/wiki/1da_Banton"], 4, 10) is None
