from abc import ABC
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, List, Tuple

from pygments.lexer import default


@dataclass
class ANode(ABC):
    key: Any
    value: Any
    color: str
    parent: Any
    left: Any
    right: Any


@dataclass
class NullNode(ANode):
    key = None
    value = None
    color = "black"
    parent = None
    left = None
    right = None


NULL = NullNode(None, None, "black", None, None, None)


@dataclass
class Node(ANode):
    key: int
    color: str = "red"
    parent: ANode = field(default_factory=NullNode)
    left: ANode = field(default_factory=NullNode)
    right: ANode = field(default_factory=NullNode)


class RBTree:
    def __init__(self) -> None:
        self.root: ANode = NULL

    def __del__(self) -> None:
        def _delete_by_rec(root: ANode) -> None:
            if root != NULL:
                _delete_by_rec(root.left)
                _delete_by_rec(root.right)
                del root

        _delete_by_rec(self.root)

    def __str__(self) -> str:
        def _get_lines(node: ANode, string: str, level: int = 0) -> str:
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
        yield from nodes

    def __setitem__(self, key: int, value: Any) -> None:
        if self.root == NULL:
            self.root = Node(key, value, "black", NULL, NULL, NULL)
            return
        tmp = self.get_node(key)
        if tmp is not NULL:
            tmp.value = value
            return
        self._insert(key, value)

    def __delitem__(self, key: int) -> None:
        if self[key] is None:
            raise KeyError("RBTree hasn't Node with this key")

        self.root, removed_node = self._remove(self.root, key)
        self._deleting_fix(removed_node)

    def _insert_fix_balance(self, new_node: ANode) -> None:
        while new_node != self.root and new_node.parent.color == "red":
            # если отец ноды - левый ребенок
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right
                if uncle.color == "red":
                    # перекрашиваем отца и дядю в черный, деда в красный
                    new_node.parent.color = uncle.color = "black"
                    new_node.parent.parent.color = "red"
                    new_node = new_node.parent.parent
                else:
                    # восстанавливаем равенство высот поворотом и меняем цвета отца и дедом
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self._rotate_left(new_node)
                    new_node.parent.color = "black"
                    new_node.parent.parent.color = "red"
                    self._rotate_right(new_node.parent.parent)
            else:
                # аналогично, но для отца = правому ребенку
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

    def _insert(self, key: int, value: Any) -> None:
        new_node = Node(key, value, "red", NULL, NULL, NULL)
        cur_node = self.root
        previous_node = cur_node
        while cur_node != NULL:
            previous_node = cur_node
            if cur_node.key == key:
                cur_node.value = value
                return
            cur_node = cur_node.left if cur_node.key > key else cur_node.right

        new_node.parent = previous_node
        if previous_node != NULL and previous_node.key < new_node.key:
            previous_node.right = new_node
        else:
            previous_node.left = new_node
        self._insert_fix_balance(new_node)

    def _deleting_fix(self, deleting_node: ANode) -> None:
        if deleting_node is None:
            return
        while deleting_node != NULL and deleting_node != self.root and deleting_node.color == "black":
            # if удаляемая нода - левый ребенок
            if deleting_node == deleting_node.parent.left:
                sibling = deleting_node.parent.right
                # брат ноды красный
                if sibling.color == "red":
                    sibling.color = "black"
                    deleting_node.parent.color = "red"
                    self._rotate_left(deleting_node.parent)
                    sibling = deleting_node.parent.right
                # брат ноды черный с черными детьми
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    deleting_node = deleting_node.parent
                else:
                    # брат ноды черный с черным правым ребенком
                    if sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self._rotate_right(sibling)
                        sibling = deleting_node.parent.right

                    # брат ноды черный с черным левым ребенком
                    sibling.color = deleting_node.parent.color
                    deleting_node.parent.color = "black"
                    sibling.right.color = "black"
                    self._rotate_left(deleting_node.parent)
                    deleting_node = self.root
            else:
                # удаляемая нода - правый ребенок. Аналогично
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

    def _remove(self, current_root: ANode, key: int, removing_node: ANode = NULL) -> Tuple[ANode, ANode]:
        if current_root.key > key:
            current_root.left, removing_node = self._remove(current_root.left, key)
        elif current_root.key < key:
            current_root.right, removing_node = self._remove(current_root.right, key)
        else:
            if current_root.left == NULL:
                return current_root.right, removing_node
            if current_root.right == NULL:
                return current_root.left, removing_node
            new_node = self.find_min_in_right_subtree(current_root)
            current_root.key, current_root.value = new_node.key, new_node.value
            removing_node = new_node
            current_root.right, removing_node = self._remove(current_root.right, current_root.key, removing_node)

        return current_root, removing_node

    def traverse(self, order: str = "pre_order") -> List[ANode]:
        nodes: List[ANode] = []

        def pre_order_traverse(node: ANode) -> None:
            if node != NULL:
                nodes.append(node)
                pre_order_traverse(node.left)
                pre_order_traverse(node.right)

        def post_order_traverse(node: ANode) -> None:
            if node != NULL:
                post_order_traverse(node.left)
                post_order_traverse(node.right)
                nodes.append(node)

        def in_order_traverse(node: ANode) -> None:
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
    def find_min_in_right_subtree(root: ANode) -> ANode:
        current_root = root.right
        if current_root == NULL:
            return root
        while current_root.left != NULL:
            current_root = current_root.left
        return current_root

    def get_node(self, key: int) -> ANode:
        curr_node: ANode = self.root
        while curr_node != NULL:
            if curr_node.key == key:
                return curr_node
            elif curr_node.key > key:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return NULL

    def _rotate_left(self, x: ANode) -> None:
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

    def _rotate_right(self, x: ANode) -> None:
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
