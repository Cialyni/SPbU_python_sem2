from abc import ABC
from typing import Mapping

import pytest

from src.Homeworks.registry import Registry

MAPPING_REGISTRY = Registry[Mapping](default=Mapping)
MAPPING_REGISTRY_WITHOUT_DEFAULT = Registry[Mapping]()


@MAPPING_REGISTRY.register(name="avl_tree")
class AVLTree(Mapping, ABC):
    pass


@MAPPING_REGISTRY.register(name="cartesian_tree")
class CartesianTree(Mapping, ABC):
    pass


@MAPPING_REGISTRY_WITHOUT_DEFAULT.register(name="some_tree")
class SomeTree:
    pass


@MAPPING_REGISTRY_WITHOUT_DEFAULT.register(name="binary_tree")
class BinaryTree:
    pass


@pytest.mark.parametrize(
    "class_name, collection",
    (
        ("avl_tree", AVLTree),
        ("cartesian_tree", CartesianTree),
    ),
)
class TestRegistryWithDefault:
    def test_registry(self, class_name: str, collection) -> None:
        test_1 = MAPPING_REGISTRY.dispatch(class_name)
        assert issubclass(test_1, collection) and issubclass(MAPPING_REGISTRY.dispatch("something_random"), Mapping)

    def test_exception_in_registry_catcher(self, class_name: str, collection) -> None:
        with pytest.raises(ValueError):
            MAPPING_REGISTRY.register(class_name)(collection)


@pytest.mark.parametrize(
    "class_name, collection",
    (
        ("binary_tree", BinaryTree),
        ("some_tree", SomeTree),
    ),
)
class TestRegistryWithoutDefault:
    def test_registry(self, class_name: str, collection) -> None:
        test_1 = MAPPING_REGISTRY_WITHOUT_DEFAULT.dispatch(class_name)
        assert issubclass(test_1, collection)

    def test_exception_in_registry_catcher(self, class_name: str, collection) -> None:
        with pytest.raises(ValueError):
            MAPPING_REGISTRY_WITHOUT_DEFAULT.register(class_name)(collection)

    def test_exception_in_dispatch(self, class_name: str, collection) -> None:
        with pytest.raises(ValueError):
            MAPPING_REGISTRY_WITHOUT_DEFAULT.dispatch("something")
