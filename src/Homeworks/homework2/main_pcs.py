from src.Homeworks.homework1.registry import Registry
from src.Homeworks.homework2.perfomans_command_storage import *

INFO = """\n(Firts word - command; i, j - indexes)\n
    Clear
    AddToEnd elem
    AddToBegin elem
    RemoveFromBegin
    RemoveFromEnd
    Replace i j
    Augment i value
    Insert i elem
    Remove i
    Reverse
    Exit
    Show
    Cancel_last
\n"""


REGISTRY = Registry[Action]()
for action in Action.__subclasses__():
    REGISTRY.register(action.__name__)(action)


def string_to_action(string: str) -> Action:
    command_lst = string.split()
    command, args = command_lst[0], command_lst[1:]
    try:
        action = REGISTRY.dispatch(command)
        try:
            args = list(map(int, args))
        except ValueError:
            print("Arguments must be INTEGER")
        else:
            return action(*args)
    except ValueError:
        print("INCORRECT COMMAND")


def create_perfomans_command_storage() -> PerformedCommandStorage:
    storage_type = input("Input your storage type\n")
    storage_data = input("Input storage data (only integers), like: 1 2 3 4 5\n")
    try:
        storage = eval(storage_type + "(map(int, storage_data.split()))")
    except ValueError:
        raise Exception("INCORRECT STORAGE DATA (need to be int)")
    except NameError:
        raise Exception("INCORRECT STORAGE TYPE")
    else:
        return PerformedCommandStorage(storage)


def main():
    print(INFO)
    try:
        pc_storage = create_perfomans_command_storage()
    except Exception as e:
        print(e)
    else:
        command = input("command:\n")
        while command != "Exit":
            try:
                if command == "Show":
                    print("Storage:", pc_storage.storage)
                elif command == "Cancel_last":
                    pc_storage.cancel_actions()
                else:
                    action = string_to_action(command)
                    pc_storage.do_actions(action)
            except Exception as e:
                print(e)
            command = input("command:\n")


if __name__ == "__main__":
    main()
