import random
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, TypeVar, Union


@dataclass
class Node:
    key: Any
    value: Any
    parent: Any
    left: Any
    right: Any
    color: str = "red"


@dataclass
class NullNode(Node):
    key = None
    value = None
    parent = None
    left = None
    right = None
    color: str = "black"


NULL = NullNode(None, None, None, None, "black")


class RBTree:
    def __init__(self) -> None:
        self.root: Node = NULL

    def __del__(self) -> None:
        def _delete_by_rec(root: Node) -> None:
            if root != NULL:
                _delete_by_rec(root.left)
                _delete_by_rec(root.right)
                del root

        _delete_by_rec(self.root)

    def __str__(self) -> str:
        def _get_lines(node: Node, string: str, level: int = 0) -> str:
            if node != NULL:
                string = _get_lines(node.right, string, level + 1)
                indent_by_depth = " " * 4 * level
                string += f"Depth: {level} {indent_by_depth}|---> ({node.key}, {node.color})\n"
                string += _get_lines(node.left, string, level + 1)
                return string
            else:
                return ""

        return _get_lines(self.root, "")

    def __contains__(self, key: int) -> bool:
        return self.get_node(key) != NULL

    def __getitem__(self, key: int) -> Any:
        needed = self.get_node(key)
        if needed == NULL:
            raise KeyError("RBTree hasn't key", key)
        return needed.value

    def __iter__(self) -> Any:
        nodes = self.traverse()
        for node in nodes:
            yield node

    def __setitem__(self, key: int, value: Any) -> None:
        if self.root == NULL:
            self.root = Node(key, value, NULL, NULL, NULL, "black")
            return

        def _insert_fix_balance(new_node: Node) -> None:
            while new_node != self.root and new_node.parent.color == "red":
                if new_node.parent == new_node.parent.parent.left:
                    uncle = new_node.parent.parent.right
                    if uncle.color == "red":
                        new_node.parent.color = uncle.color = "black"
                        new_node.parent.parent.color = "red"
                        new_node = new_node.parent.parent
                    else:
                        if new_node == new_node.parent.right:
                            new_node = new_node.parent
                            self._rotate_left(new_node)
                        new_node.parent.color = "black"
                        new_node.parent.parent.color = "red"
                        self._rotate_right(new_node.parent.parent)
                else:
                    uncle = new_node.parent.parent.left
                    if uncle.color == "red":
                        new_node.parent.color = uncle.color = "black"
                        new_node.parent.parent.color = "red"
                        new_node = new_node.parent.parent
                    else:
                        if new_node == new_node.parent.left:
                            new_node = new_node.parent
                            self._rotate_right(new_node)
                        new_node.parent.color = "black"
                        new_node.parent.parent.color = "red"
                        self._rotate_left(new_node.parent.parent)
            self.root.color = "black"

        def _insert(key: int, value: Any) -> None:
            new_node = Node(key, value, NULL, NULL, NULL)
            cur_node = self.root
            previous_node: Node
            while cur_node != NULL:
                previous_node = cur_node
                if cur_node.key == key:
                    cur_node.value = value
                    return
                cur_node = cur_node.left if cur_node.key > key else cur_node.right

            new_node.parent = previous_node
            if previous_node.key < new_node.key:
                previous_node.right = new_node
            else:
                previous_node.left = new_node
            _insert_fix_balance(new_node)

        _insert(key, value)

    def __delitem__(self, key: int) -> None:
        if self[key] is None:
            raise KeyError("RBTree hasn't Node with this key")

        def _deleting_fix(deleting_node: Node) -> None:
            if deleting_node is None:
                return
            while deleting_node != self.root and deleting_node.color == "black":
                if deleting_node == deleting_node.parent.left:
                    sibling = deleting_node.parent.right
                    if sibling.color == "red":
                        sibling.color = "black"
                        deleting_node.parent.color = "red"
                        self._rotate_left(deleting_node.parent)
                        sibling = deleting_node.parent.right

                    if sibling.left.color == "black" and sibling.right.color == "black":
                        sibling.color = "red"
                        deleting_node = deleting_node.parent
                    else:
                        if sibling.right.color == "black":
                            sibling.left.color = "black"
                            sibling.color = "red"
                            self._rotate_right(sibling)
                            sibling = deleting_node.parent.right

                        sibling.color = deleting_node.parent.color
                        deleting_node.parent.color = "black"
                        sibling.right.color = "black"
                        self._rotate_left(deleting_node.parent)
                        deleting_node = self.root
                else:
                    sibling = deleting_node.parent.left
                    if sibling.color == "red":
                        sibling.color = "black"
                        deleting_node.parent.color = "red"
                        self._rotate_right(deleting_node.parent)
                        sibling = deleting_node.parent.left

                    if sibling.left.color == "black" and sibling.right.color == "black":
                        sibling.color = "red"
                        deleting_node = deleting_node.parent
                    else:
                        if sibling.left.color == "black":
                            sibling.right.color = "black"
                            sibling.color = "red"
                            self._rotate_left(sibling)
                            sibling = deleting_node.parent.left

                        sibling.color = deleting_node.parent.color
                        deleting_node.parent.color = "black"
                        sibling.left.color = "black"
                        self._rotate_right(deleting_node.parent)
                        deleting_node = self.root
            deleting_node.color = "black"

        def _remove(current_root: Node, key: int, removing_node: Node = NULL) -> Tuple[Node, Node]:
            if current_root.key > key:
                current_root.left, removing_node = _remove(current_root.left, key)
            elif current_root.key < key:
                current_root.right, removing_node = _remove(current_root.right, key)
            else:
                if current_root.left == NULL:
                    return current_root.right, removing_node
                if current_root.right == NULL:
                    return current_root.left, removing_node
                new_node = self.find_min_in_right_subtree(current_root)
                current_root.key, current_root.value = new_node.key, new_node.value
                removing_node = new_node
                current_root.right, removing_node = _remove(current_root.right, current_root.key, removing_node)

            return current_root, removing_node

        self.root, removed_node = _remove(self.root, key)
        _deleting_fix(removed_node)

    def traverse(self, order: str = "pre_order") -> List[Node]:
        nodes: List[Node] = []

        def pre_order_traverse(node: Node) -> None:
            if node != NULL:
                nodes.append(node)
                pre_order_traverse(node.left)
                pre_order_traverse(node.right)

        def post_order_traverse(node: Node) -> None:
            if node != NULL:
                post_order_traverse(node.left)
                post_order_traverse(node.right)
                nodes.append(node)

        def in_order_traverse(node: Node) -> None:
            if node != NULL:
                in_order_traverse(node.left)
                nodes.append(node)
                in_order_traverse(node.right)

        if order == "pre_order":
            pre_order_traverse(self.root)
        if order == "post_order":
            post_order_traverse(self.root)
        if order == "in_order":
            in_order_traverse(self.root)
        return nodes

    @staticmethod
    def find_min_in_right_subtree(root: Node) -> Node:
        current_root = root.right
        if current_root == NULL:
            return root
        while current_root.left != NULL:
            current_root = current_root.left
        return current_root

    def get_node(self, key: int) -> Node:
        curr_node: Node = self.root
        while curr_node != NULL:
            if curr_node.key == key:
                return curr_node
            elif curr_node.key > key:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return NULL

    def _rotate_left(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left != NULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == NULL:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: Node) -> None:
        y = x.left
        x.left = y.right
        if y.right != NULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == NULL:
            self.root = y
        else:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        y.right = x
        x.parent = y


a = RBTree()
a[1] = 1
a[2] = 2
a[3] = 3
print(a)
