import random
from io import StringIO

import pytest

from src.Homeworks.homework2.main_pcs import *
from src.Homeworks.homework2.perfomans_command_storage import *

TEST_COLLECTION = [1, 2, 3, 4, 5]
PCS = PerformedCommandStorage(TEST_COLLECTION)


class TestActions:
    def test_clear(self):
        act = Clear()
        PCS.do_actions(act)
        assert len(PCS.storage) == 0
        PCS.cancel_actions()
        assert len(PCS.storage) == len(TEST_COLLECTION)

    def test_add_to_begin(self):
        elem = 0
        act = AddToBegin(elem)
        old_len = len(PCS.storage)
        PCS.do_actions(act)
        assert PCS.storage[0] == elem and len(PCS.storage) == old_len + 1
        PCS.cancel_actions()
        assert PCS.storage[0] != elem and len(PCS.storage) == old_len

    def test_add_to_end(self):
        elem = 0
        act = AddToEnd(elem)
        old_len = len(PCS.storage)
        PCS.do_actions(act)
        assert PCS.storage[-1] == elem and len(PCS.storage) == old_len + 1
        PCS.cancel_actions()
        assert PCS.storage[-1] != elem and len(PCS.storage) == old_len

    def test_remove_from_begin(self):
        act = RemoveFromBegin()
        old_len = len(PCS.storage)
        first = PCS.storage[0]
        PCS.do_actions(act)
        assert PCS.storage[0] != first and len(PCS.storage) == old_len - 1
        PCS.cancel_actions()
        assert PCS.storage[0] == first and len(PCS.storage) == old_len

    def test_remove_from_end(self):
        act = RemoveFromEnd()
        old_len = len(PCS.storage)
        last = PCS.storage[-1]
        PCS.do_actions(act)
        assert PCS.storage[-1] != last and len(PCS.storage) == old_len - 1
        PCS.cancel_actions()
        assert PCS.storage[-1] == last and len(PCS.storage) == old_len

    def test_replace(self):
        i, j = random.randint(0, len(PCS.storage) // 2), random.randint(len(PCS.storage) // 2 + 1, len(PCS.storage) - 1)
        elem_i = PCS.storage[i]
        act = Replace(i, j)
        PCS.do_actions(act)
        assert PCS.storage[j] == elem_i and PCS.storage[i] != elem_i
        PCS.cancel_actions()
        assert PCS.storage[i] == elem_i and PCS.storage[j] != elem_i

    def test_augment(self):
        delta = random.randint(-100000, 100000)
        i = random.randint(0, len(PCS.storage) - 1)
        old_value = PCS.storage[i]
        act = Augment(i, delta)
        PCS.do_actions(act)
        assert PCS.storage[i] == old_value + delta
        PCS.cancel_actions()
        assert PCS.storage[i] == old_value

    def test_insert(self):
        elem = random.randint(-10000, 10000)
        i = random.randint(0, len(PCS.storage) - 1)
        old_len = len(PCS.storage)
        act = Insert(i, elem)
        PCS.do_actions(act)
        assert PCS.storage[i] == elem and len(PCS.storage) == old_len + 1
        PCS.cancel_actions()
        assert PCS.storage[i] != elem and len(PCS.storage) == old_len

    def test_remove(self):
        i = random.randint(0, len(PCS.storage) - 2)
        old_len = len(PCS.storage)
        old_elem = PCS.storage[i]
        act = Remove(i)
        PCS.do_actions(act)
        assert PCS.storage[i] != old_elem and len(PCS.storage) == old_len - 1
        PCS.cancel_actions()
        assert PCS.storage[i] == old_elem and len(PCS.storage) == old_len


@pytest.mark.parametrize(
    "user_input, expected_output",
    [
        (["aboba", "1 2 3 4 5"], [INFO, "INCORRECT STORAGE TYPE\n"]),
        (["list", "1 2 aboba 4 5"], [INFO, "INCORRECT STORAGE DATA (need to be int)\n"]),
        (
            ["list", "1 2 3 4 5", "AddToBegin 0", "Show", "Exit"],
            [INFO, "Storage: [0, 1, 2, 3, 4, 5]\n"],
        ),
        (
            ["list", "1 2 3 4 5", "Cancel_last", "Show", "Exit"],
            [INFO, "Nothing to cancel", "Storage: [1, 2, 3, 4, 5]\n"],
        ),
        (
            ["list", "1 2 3 4 5", "Insert -1 -1", "Clear", "Show", "Cancel_last", "Show", "Exit"],
            [INFO, "i need to be: 0 <= i < len(storage)", "Storage: []", "Storage: [1, 2, 3, 4, 5]\n"],
        ),
    ],
)
def test_main(monkeypatch, user_input: List[str], expected_output: List[str]) -> None:
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    assert output == "\n".join(expected_output)
