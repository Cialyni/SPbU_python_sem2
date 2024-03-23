from typing import Any, OrderedDict, Mapping

import pytest
from src.Homeworks.Registry import Registry


MAPPING_REGISTRY = Registry[Mapping](default=dict)
MAPPING_REGISTRY_WITHOUT_DEFAULT = Registry[Mapping]()


@MAPPING_REGISTRY.register(name="avl_tree")
class AVLTree(Mapping):
    pass


@MAPPING_REGISTRY.register(name="cartesian_tree")
class CartesianTree(Mapping):
    pass


def test_registry():
    test_1 = MAPPING_REGISTRY.dispatch("avl_tree")
    assert issubclass(test_1, AVLTree)
    test_2 = MAPPING_REGISTRY.dispatch("unknown_tree")
    assert issubclass(test_2, dict)


def test_exception_in_registry():
    with pytest.raises(ValueError):
        MAPPING_REGISTRY.register("avl_tree")(AVLTree)


def test_exception_in_dispatch():
    with pytest.raises(ValueError):
        MAPPING_REGISTRY_WITHOUT_DEFAULT.dispatch(name="aboba")
