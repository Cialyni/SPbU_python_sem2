from typing import Any, List, MutableSequence, Optional


class Action:
    def straight_action(self, storage: MutableSequence[int]):
        raise NotImplementedError()

    def reverse_action(self, storage: MutableSequence[int]):
        raise NotImplementedError()


class DeleteAll(Action):
    def __init__(self):
        self.storage: Optional[MutableSequence[int]] = None

    def straight_action(self, storage: MutableSequence[int]):
        self.storage = storage
        storage = []

    def reverse_action(self, storage: MutableSequence[int]):
        storage = self.storage


class AddToBegin(Action):
    def __init__(self, elem: int):
        self.elem = elem

    def straight_action(self, storage: MutableSequence[int]):
        storage.insert(0, self.elem)

    def reverse_action(self, storage: MutableSequence[Any]):
        storage.pop(0)


class AddToEnd(Action):
    def __init__(self, elem: int):
        self.elem = elem

    def straight_action(self, storage: MutableSequence[int]):
        storage.append(self.elem)

    def reverse_action(self, storage: MutableSequence[int]):
        storage.pop()


class RemoveFromBegin(Action):
    def __init__(self):
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]):
        self.removed_elem = storage.pop()

    def reverse_action(self, storage: MutableSequence[Any]):
        storage.insert(0, self.removed_elem)


class RemoveFromEnd(Action):
    def __init__(self):
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]):
        self.removed_elem = storage.pop()

    def reverse_action(self, storage: MutableSequence[int]):
        storage.append(self.removed_elem)


class Replace(Action):
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j

    def straight_action(self, storage: MutableSequence[int]):
        i = self.i
        while i != self.j:
            storage[i], storage[i + 1] = storage[i + 1], storage[i]
            i += 1

    def reverse_action(self, storage: MutableSequence[int]):
        j = self.j
        while j != self.i:
            storage[j], storage[j - 1] = storage[j - 1], storage[j]
            j -= 1


class Augment(Action):
    def __init__(self, i: int, value: int):
        self.i = i
        self.value = value

    def straight_action(self, storage: MutableSequence[int]):
        storage[self.i] += self.value

    def reverse_action(self, storage: MutableSequence[int]):
        storage[self.i] -= self.value


class Insert(Action):
    def __init__(self, i: int, elem: int):
        self.i = i
        self.insertion_elem = elem

    def straight_action(self, storage: MutableSequence[int]):
        storage.insert(self.i, self.insertion_elem)

    def reverse_action(self, storage: MutableSequence[int]):
        storage.pop(self.i)


class Remove(Action):
    def __init__(self, i: int):
        self.i = i
        self.removed_elem = None

    def straight_action(self, storage: MutableSequence[int]):
        self.removed_elem = storage.pop(self.i)

    def reverse_action(self, storage: MutableSequence[int]):
        storage.insert(self.i, self.removed_elem)


class Reverse(Action):
    def straight_action(self, storage: MutableSequence[int]):
        storage.reverse()

    def reverse_action(self, storage: MutableSequence[int]):
        storage.reverse()


class PerformedCommandStorage:
    def __init__(self, sequence: MutableSequence[int]):
        self.action_log: List[Action] = []
        self.storage: MutableSequence[int] = sequence

    def do_actions(self, action: Action):
        self.action_log.append(action)
        action.straight_action(self.storage)

    def cancel_actions(self):
        if len(self.action_log) > 0:
            undo = self.action_log.pop()
            undo.reverse_action(self.storage)
        else:
            raise AttributeError("Nothing to cancel")


def command_to_action(string: str):
    string_lst = string.split()
    if string_lst[0] == "add_to_begin":
        action = AddToBegin(int(string_lst[1]))
    elif string_lst[0] == "add_to_end":
        action = AddToEnd(int(string_lst[1]))
    elif string_lst[0] == "insert":
        action = Insert(int(string_lst[1]), int(string_lst[2]))
    elif string_lst[0] == "augment":
        action = Augment(int(string_lst[1]), int(string_lst[2]))
    else:
        raise NotImplementedError("This function doesnt exit. Check name correctness")
    return action


def info():
    print(
        "'''\n   (Firts word - command; i, j - indexes)\n"
        "   add_to_begin elem\n"
        "   add_to_end elem\n"
        "   insert i j\n"
        "   augment i value\n"
        "   Input exit to exit\n"
        "   Input get_storage to get storage\n"
        "   Input cancel_last to cancel last action\n"
        "'''\n"
    )


if __name__ == "__main__":
    info()
    lst = list(map(int, input("Input your storage with space\n").split()))
    storage = PerformedCommandStorage(lst)
    command = input("Input command\n")
    while command != "exit":
        if command == "get_storage":
            print(storage.storage)
        elif command == "cancel_last":
            storage.cancel_actions()
        else:
            action = command_to_action(command)
            storage.add_action(action)
            storage.do_actions()
        command = input("Input command\n")
