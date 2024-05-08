from copy import copy
from typing import Any, List, MutableSequence, Optional


class Action:
    def straight_action(self, storage: MutableSequence[int]) -> None:
        raise NotImplementedError()

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        raise NotImplementedError()


class Clear(Action):
    def __init__(self) -> None:
        self.storage: Optional[MutableSequence[int]] = None

    def straight_action(self, storage: MutableSequence[int]) -> None:
        self.storage = copy(storage)
        storage.clear()

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage += self.storage


class AddToBegin(Action):
    def __init__(self, elem: int) -> None:
        self.elem = elem

    def straight_action(self, storage: MutableSequence[int]) -> None:
        storage.insert(0, self.elem)

    def reverse_action(self, storage: MutableSequence[Any]) -> None:
        storage.pop(0)


class AddToEnd(Action):
    def __init__(self, elem: int) -> None:
        self.elem = elem

    def straight_action(self, storage: MutableSequence[int]) -> None:
        storage.append(self.elem)

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage.pop()


class RemoveFromBegin(Action):
    def __init__(self) -> None:
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]) -> None:
        self.removed_elem = storage.pop(0)

    def reverse_action(self, storage: MutableSequence[Any]) -> None:
        storage.insert(0, self.removed_elem)


class RemoveFromEnd(Action):
    def __init__(self) -> None:
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]) -> None:
        self.removed_elem = storage.pop()

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage.append(self.removed_elem)


class Replace(Action):
    def __init__(self, i: int, j: int) -> None:
        self.i = i
        self.j = j

    def straight_action(self, storage: MutableSequence[int]) -> None:
        if not (0 <= self.i < self.j < len(storage)):
            raise ValueError("i, j need to be: 0 <= i < j < len(storage)")
        i = self.i
        while i != self.j:
            storage[i], storage[i + 1] = storage[i + 1], storage[i]
            i += 1

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        j = self.j
        while j != self.i:
            storage[j], storage[j - 1] = storage[j - 1], storage[j]
            j -= 1


class Augment(Action):
    def __init__(self, i: int, value: int) -> None:
        self.i = i
        self.value = value

    def straight_action(self, storage: MutableSequence[int]) -> None:
        if not (0 <= self.i < len(storage)):
            raise ValueError("i need to be: 0 <= i < len(storage)")
        storage[self.i] += self.value

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage[self.i] -= self.value


class Insert(Action):
    def __init__(self, i: int, elem: int) -> None:
        self.i = i
        self.insertion_elem = elem

    def straight_action(self, storage: MutableSequence[int]) -> None:
        if not (0 <= self.i < len(storage)):
            raise ValueError("i need to be: 0 <= i < len(storage)")
        storage.insert(self.i, self.insertion_elem)

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage.pop(self.i)


class Remove(Action):
    def __init__(self, i: int) -> None:
        self.i = i
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]) -> None:
        if not (0 <= self.i < len(storage)):
            raise ValueError("i need to be: 0 <= i < len(storage)")
        self.removed_elem = storage.pop(self.i)

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage.insert(self.i, self.removed_elem)


class Reverse(Action):
    def straight_action(self, storage: MutableSequence[int]) -> None:
        storage.reverse()

    def reverse_action(self, storage: MutableSequence[int]) -> None:
        storage.reverse()


class PerformedCommandStorage:
    def __init__(self, sequence: MutableSequence[int]) -> None:
        self.action_log: List[Action] = []
        self.storage: MutableSequence[int] = sequence

    def do_actions(self, action: Action) -> None:
        self.action_log.append(action)
        action.straight_action(self.storage)

    def cancel_actions(self) -> None:
        if len(self.action_log) > 0:
            canceled = self.action_log.pop()
            canceled.reverse_action(self.storage)
        else:
            raise AttributeError("Nothing to cancel")
