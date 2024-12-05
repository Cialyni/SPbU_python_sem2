import random

import pytest

from src.Commission.RedBlackTree import NULL, Node, RBTree


class TestRBTree:
    @staticmethod
    def get_black_height(tree: RBTree) -> int:
        black_height = 0
        cur_root = tree.root
        while cur_root is not NULL:
            cur_root = cur_root.left
            if cur_root is not NULL and cur_root.color == "black":
                black_height += 1
        return black_height

    def check_black_height_equality(self, tree):
        black_height = self.get_black_height(tree)

        def _dfs_compare_black_height(root: Node, black_height: int, cur_node_black_height: int):
            if root is not NULL:
                if root.color == "black":
                    cur_node_black_height += 1
                return _dfs_compare_black_height(
                    root.left, black_height, cur_node_black_height
                ) and _dfs_compare_black_height(root.right, black_height, cur_node_black_height)
            else:
                if black_height != cur_node_black_height:

                    return False
            return True

        return _dfs_compare_black_height(tree.root, black_height, -1)

    @staticmethod
    def build_random_RBTree(size: int = random.randint(10, 10), a=-int(1e6), b=int(1e6)) -> RBTree:
        new_RBTree = RBTree()
        for i in range(size):
            key = random.randint(a, b)
            value = random.randint(a, b)
            new_RBTree[key] = value

        return new_RBTree

    def check_tree_invariant(self, tree: RBTree) -> bool:
        def _recursion_check(curr_root: Node) -> bool:
            left_res, right_res = True, True
            if curr_root is NULL or curr_root.left is NULL and curr_root.right is NULL:
                return True
            if curr_root.left is not NULL:
                left_res = (
                    curr_root.key >= curr_root.left.key and not (curr_root.color == curr_root.left.color == "red")
                ) and _recursion_check(curr_root.left)
            if curr_root.right is not NULL:
                right_res = (
                    curr_root.key <= curr_root.right.key and not (curr_root.color == curr_root.right.color == "red")
                ) and _recursion_check(curr_root.right)
            return left_res and right_res

        return _recursion_check(tree.root) and self.check_black_height_equality(tree)

    def test_setitem(self):
        tree = self.build_random_RBTree()
        """
        print(self.check_tree_invariant(tree))
        print(self.check_black_height_equality(tree))
        print(self.get_black_height(tree))
        print(tree)
        """
        assert self.check_tree_invariant(tree)

    @pytest.mark.parametrize(
        "keys, values",
        (
            ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ("adsf", "31", 1, "hft", "1", "222222", (2, 4, 5), 3333, 9, "10")),
            ((1, 1, 1), ("1", "11", "111")),
            ((-444558776671, 5141414, 0, 11, 56), ("ammlxv", "5141414", (0, 0), ("11",), (5, 6))),
        ),
    )
    def test_getitem_and_contains(self, keys, values):
        tree = RBTree()
        for i, key in enumerate(keys):
            tree[key] = values[i]
            assert tree[key] == values[i]
            assert key in tree

    def test_delitem(self):
        for i in range(5):
            tree = self.build_random_RBTree()
            deleting_key = random.randint(-int(1e6), int(1e6))
            tree[deleting_key] = "some_value"
            del tree[deleting_key]
            assert self.check_tree_invariant(tree)
            assert deleting_key not in tree

    def test_iter(self):
        d = self.build_random_RBTree()
        nodes = d.traverse()
        for i, node in enumerate(d):
            assert node == nodes[i]
