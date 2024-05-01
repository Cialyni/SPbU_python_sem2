from src.Homeworks.homework2.perfomans_command_storage import *
from src.Homeworks.homework1.registry import Registry


def info():
    print(
        "'''\n   (Firts word - command; i, j - indexes)\n"
        "    elem\n"
        "   Clear\n"
        "   AddToEnd elem\n"
        "   AddToBegin elem\n"
        "   RemoveFromBegin\n"
        "   RemoveFromEnd\n"
        "   Replace i j\n "
        "   Augment i value\n"
        "   Insert i elem\n"
        "   Remove i"
        "   Reverse\n"
        "   Input exit to exit\n"
        "   Input get_storage to get storage\n"
        "   Input cancel_last to cancel last action\n"
        "'''\n"
    )


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
        print("INCORRECT STORAGE DATA (need to be int)")
    except SyntaxError:
        print("INCORRECT STORAGE TYPE")
    else:
        return PerformedCommandStorage(storage)


if __name__ == "__main__":
    info()
    try:
        pc_storage = create_perfomans_command_storage()
    except Exception as e:
        print(e)
    else:
        command = input("command")
        while command != "exit":
            try:
                action = string_to_action(command)
                pc_storage.do_actions(action)
            except Exception as e:
                print(e)
            command = input("command")
