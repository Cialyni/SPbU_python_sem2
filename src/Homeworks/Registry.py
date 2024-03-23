from typing import OrderedDict, Any, Dict, Type, TypeVar, Generic

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, default: Type[T] = None):
        self.store: Dict[str, T] = {}
        self.default = default

    def register(self, name: str):
        if name in self.store:
            raise ValueError(f"{name} already in registry")

        def deco(cls: Type[T]):
            self.store[name] = cls
            return cls

        return deco

    def dispatch(self, name: str):
        if name in self.store:
            return self.store[name]
        elif self.default is not None:
            return self.default
        else:
            return ValueError(f"{name} doesn't in registry")


if __name__ == "__main__":
    mapping_registry = Registry[Any]("Any")
    mapping_registry.register("tuple")(tuple)
    mapping_registry.register("ordered_dict")(OrderedDict)
    print("Now checking registry working:\n")
    try:
        assert mapping_registry.dispatch("tuple") == tuple
        assert mapping_registry.dispatch("aboba") == "Any"
        assert mapping_registry.dispatch("ordered_dict") == OrderedDict

    except:
        print("Something going wrong")
