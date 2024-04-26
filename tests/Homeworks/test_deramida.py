import pytest

from src.Homeworks.deramida import Deramida, merge, split

TEST_DERAMIDA = Deramida()


@pytest.mark.parametrize("key, value", ((1, 1), (-1, "aboba"), (1.5, "gerrggs"), (10, -1)))
def test_get_and_set(key, value):
    TEST_DERAMIDA[key] = value
    assert TEST_DERAMIDA[key] == value


def test_del():
    print(TEST_DERAMIDA.root)
    del TEST_DERAMIDA[1]
    assert 1 in TEST_DERAMIDA
    del TEST_DERAMIDA[1.5]
    assert 1.5 in TEST_DERAMIDA
    with pytest.raises(KeyError):
        del TEST_DERAMIDA[9999999]
