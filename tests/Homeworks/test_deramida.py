import copy
import random

import pytest

from src.Homeworks.deramida import Deramida, Node, merge, split


class TestDeramida:
    @staticmethod
    def build_random_tree(size: int = random.randint(0, 10000), a=-int(1e6), b=int(1e6)) -> Deramida:
        new_deramida = Deramida()
        for i in range(size):
            key = random.randint(a, b)
            value = random.randint(a, b)
            new_deramida[key] = value

        return new_deramida

    @staticmethod
    def check_tree_invariant(tree: Deramida) -> bool:
        def _recursion_check(curr_root: Node) -> bool:
            left_res, right_res = True, True
            if curr_root is None or curr_root.left is None and curr_root.right is None:
                return True
            if curr_root.left is not None:
                left_res = (
                    curr_root.priority > curr_root.left.priority and curr_root.key > curr_root.left.key
                ) and _recursion_check(curr_root.left)
            if curr_root.right is not None:
                right_res = (
                    curr_root.priority > curr_root.right.priority and curr_root.key < curr_root.right.key
                ) and _recursion_check(curr_root.right)
            return left_res and right_res

        return _recursion_check(tree.root)

    def test_merge(self):
        for i in range(5):
            d1, d2 = self.build_random_tree(b=0), self.build_random_tree(a=0)
            d3 = merge(copy.deepcopy(d1), copy.deepcopy(d2))
            assert self.check_tree_invariant(d3)
            existence_flag = True
            nodes_d1, nodes_d2 = d1.traverse(), d2.traverse()
            for node in nodes_d1:
                if d3[node.key] != d1[node.key]:
                    existence_flag = False
            for node in nodes_d2:
                if d3[node.key] != d2[node.key]:
                    existence_flag = False
            assert existence_flag

    def test_split(self):
        for i in range(5):
            d = self.build_random_tree()
            split_key = random.randint(-int(1e6), int(1e6))
            d1, d2 = split(copy.deepcopy(d), split_key)
            assert self.check_tree_invariant(d1) and self.check_tree_invariant(d2)
            keys_invariant_flag = True
            nodes_d1, nodes_d2 = d1.traverse(), d2.traverse()
            for node in nodes_d1:
                if node.key >= split_key:
                    keys_invariant_flag = False
            for node in nodes_d2:
                if node.key <= split_key:
                    keys_invariant_flag = False
            assert keys_invariant_flag

    def test_setitem(self):
        d = self.build_random_tree()
        assert self.check_tree_invariant(d)

    @pytest.mark.parametrize(
        "keys, values",
        (
            ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ("adsf", "31", 1, "hft", "1", "222222", (2, 4, 5), 3333, 9, "10")),
            ((1, 1, 1), ("1", "11", "111")),
            ((-444558776671, 5141414, 0, 11, 56), ("ammlxv", "5141414", (0, 0), ("11",), (5, 6))),
        ),
    )
    def test_getitem_and_contains(self, keys, values):
        d = Deramida()
        for i, key in enumerate(keys):
            d[key] = values[i]
            assert d[key] == values[i]
            assert key in d

    def test_delitem(self):
        for i in range(5):
            d = self.build_random_tree()
            deleted_keys = random.randint(-int(1e6), int(1e6))
            d[deleted_keys] = "some_value"
            d_len = len(d)
            del d[deleted_keys]
            assert self.check_tree_invariant(d)
            assert (len(d) == d_len - 1) and deleted_keys not in d

    def test_iter(self):
        d = self.build_random_tree()
        nodes = d.traverse()
        for i, node in enumerate(d):
            assert node == nodes[i]
