from typing import Callable, Counter, Dict, Generic, Mapping, Optional, OrderedDict, Type, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, default: Optional[Type[T]] = None):
        self.store: Dict[str, Type[T]] = {}
        self.default = default

    def register(self, name: str) -> Callable[[Type[T]], Type[T]]:
        if name in self.store:
            raise ValueError(f"{name} already in registry")

        def deco(cls: Type[T]) -> Type[T]:
            self.store[name] = cls
            return cls

        return deco

    def dispatch(self, name: str) -> Type[T]:
        if name in self.store:
            return self.store[name]
        elif self.default is not None:
            return self.default
        else:
            raise ValueError(f"{name} doesn't in registry")


if __name__ == "__main__":
    mapping_registry = Registry[Mapping](Mapping)
    s = input("Enter 1 if you want to registry dict\nEnter 2 if you want to registry tuple")
    if s == "1":
        mapping_registry.register("OrderedDict")(OrderedDict)
    if s == "2":
        mapping_registry.register("Counter")(Counter)
    print("Now something in registry :)")
    print(mapping_registry.dispatch("OrderedDict"))
    print(mapping_registry.dispatch("Counter"))
