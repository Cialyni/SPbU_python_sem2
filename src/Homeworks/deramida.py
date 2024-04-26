from random import randint
from typing import Any, Generic, List, MutableMapping, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Printer:
    def __init__(self):
        self.root = None

    def __str__(self):
        string = [""]

        def _get_lines(node, level=0):
            if node is not None:
                _get_lines(node.left, level + 1)
                string[0] += f"Depth: {level} {" " * 4 * level}|---> ({node.priority}, {node.key})\n"
                _get_lines(node.right, level + 1)

        _get_lines(self.root)
        return string[0]

    """        for i in _get_lines(self.root):
            print(*i, sep="")"""

    def __repr__(self):
        def _get_nodes(curr_root):
            if curr_root.left is None and curr_root.right is None:
                return (
                    f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, left=None, "
                    f"right=None)"
                )
            curr_repr = f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, "
            curr_repr += f"left={_get_nodes(curr_root.left)}, " if curr_root.left is not None else "left=None, "
            curr_repr += f"right={_get_nodes(curr_root.right)})" if curr_root.right is not None else "right=None)"
            return curr_repr

        return _get_nodes(self.root)


class NodeComparator:
    def __init__(self):
        self.key = None
        self.priority = None

    def __lt__(self, other):
        if self is None:
            return other is not None
        if other is None:
            return False

        if self.priority > other.priority:
            return False
        elif self.priority < other.priority:
            return True
        else:
            return self.key < other.key

    def __gt__(self, other):
        return not (self < other)

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return self.priority == other.priority and self.key == other.key


class Node(NodeComparator):
    def __init__(self, key=None, value=None):
        self.priority: int = randint(0, int(1e9))
        self.key: K = key
        self.value: V = value
        self.left = None
        self.right = None

    def __str__(self):
        return f"priority={self.priority}, key={self.key}, value={self.value}"


class Deramida(MutableMapping, Printer, Generic[K, V]):
    def __init__(self, node: Node = None):
        self.root: Node = node
        self.len = 1 if node else 0

    def __getitem__(self, key: K) -> V:
        needed = self.get_node(key)
        if needed is None or needed.key != key:
            raise KeyError
        return needed.value

    def __contains__(self, key: K):
        try:
            return True if self[key] is not None else False
        except KeyError:
            return False

    def get_node(self, key: K) -> Node | None:
        curr_node = self.root
        while curr_node is not None:
            if curr_node.key == key:
                return curr_node
            elif curr_node.key > key:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    def traverse(self, order: str = "pre_order") -> List[Node]:
        nodes = []

        def pre_order_traverse(node) -> None:
            if node is not None:
                nodes.append(node)
                pre_order_traverse(node.left)
                pre_order_traverse(node.right)

        def post_order_traverse(node) -> None:
            if node is not None:
                post_order_traverse(node.left)
                post_order_traverse(node.right)
                nodes.append(node)

        def in_order_traverse(node) -> None:
            if node is not None:
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

    def __eq__(self, other):
        nodes1, nodes2 = self.traverse(), other.traverse()
        return nodes1 == nodes2

    def __setitem__(self, key: K, value: V) -> None:
        if key in self:
            del self[key]

        d1, d2 = split(self, key)
        new_node = Node(key, value)
        new_d = Deramida(new_node)
        d2 = merge(new_d, d2)
        self.root = merge(d1, d2).root
        self.len += 1

    def __delitem__(self, key: K) -> None:
        deleting = self.get_node(key)
        if deleting is None:
            raise KeyError(f"There no {key} in Deramida")
        d1, d2 = split(self, key)
        del deleting
        self.root = merge(d1, d2).root
        self.len -= 1

    def __iter__(self) -> Any:
        nodes = self.traverse()
        for node in nodes:
            yield node

    def __len__(self) -> int:
        return self.len


def merge(d1: Deramida, d2: Deramida) -> Deramida:  # all keys in d1 need to be smaller than all key in d2
    def _merge(rt1: Node, rt2: Node) -> Node:
        if rt1 is None:
            return rt2
        if rt2 is None:
            return rt1
        if rt1.priority > rt2.priority:
            rt1.right = _merge(rt1.right, rt2)
            return rt1
        else:
            rt2.left = _merge(rt1, rt2.left)
            return rt2

    if d1 is None:
        return d2
    if d2 is None:
        return d1
    new_root = _merge(d1.root, d2.root)
    return Deramida(new_root)


def split(d: Deramida, key: K) -> (Deramida, Deramida):  # Left deramida keys < key  |  Right deramida keys > key
    def _split(rt: Node) -> (Node, Node):
        if rt is None:
            return None, None
        if rt.key < key:
            d1_rt, d2_rt = _split(rt.right)
            rt.right = d1_rt
            return rt, d2_rt
        elif rt.key > key:
            d1_rt, d2_rt = _split(rt.left)
            rt.left = d2_rt
            return d1_rt, rt
        return rt.left, rt.right

    if d is None:
        return None, None
    rt1, rt2 = _split(d.root)
    return Deramida(rt1), Deramida(rt2)


if __name__ == "__main__":
    deramida = Deramida()
    deramida[6] = "aboba"
    deramida[5] = "hihihaha"
    deramida[100] = 100
    deramida[52] = 62
    deramida[14] = 45
    deramida[100] = 74
    deramida[86] = 2
    deramida[5] = 10340
    deramida[74] = 1
    deramida[23] = 53
    deramida[211] = 100
    deramida[3] = 0
    print(len(deramida))
    print(deramida)

    for i in deramida:
        print(i)
