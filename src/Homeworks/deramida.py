from random import randint
from typing import Any, Generic, Iterable, List, MutableMapping, Optional, Tuple, TypeVar, Union

K = TypeVar("K")
V = TypeVar("V")


class PrinterMixin:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def __str__(self) -> str:
        string = [""]

        def _get_lines(node: Optional[Node], level: int = 0) -> None:
            if node is not None:
                _get_lines(node.left, level + 1)
                indent_by_depth = " " * 4 * level
                string[0] += f"Depth: {level} {indent_by_depth}|---> ({node.priority}, {node.key})\n"
                _get_lines(node.right, level + 1)

        _get_lines(self.root)
        return string[0]

    def __repr__(self) -> str:
        def _get_nodes(curr_root: Union[Node, Any]) -> str:
            if curr_root.left is None and curr_root.right is None:
                return f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, left=None, right=None)"
            curr_repr = f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, "
            curr_repr += f"left={_get_nodes(curr_root.left)}, " if curr_root.left is not None else "left=None, "
            curr_repr += f"right={_get_nodes(curr_root.right)})" if curr_root.right is not None else "right=None)"
            return curr_repr

        return _get_nodes(self.root)


class NodeComparator(Generic[K]):
    def __init__(self) -> None:
        self.key: Optional[K] = None
        self.priority: int

    def __lt__(self, other: "Node") -> bool:
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

    def __gt__(self, other: "Node") -> bool:
        return not (self < other)

    def __eq__(self, other: "Node") -> bool:    # type: ignore[override]
        if not isinstance(other, NodeComparator):
            return NotImplemented
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return self.priority == other.priority and self.key == other.key


class Node(NodeComparator, Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.priority: int = randint(0, int(1e9))
        self.key: K = key
        self.value: V = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __str__(self) -> str:
        return f"priority={self.priority}, key={self.key}, value={self.value}"


class Deramida(MutableMapping, PrinterMixin, Generic[K, V]):
    def __init__(self, node: Optional[Node] = None) -> None:
        self.root: Optional[Node] = node
        self.len = 1 if node else 0

    def __getitem__(self, key: K) -> V:
        needed = self.get_node(key)
        if needed is None or needed.key != key:
            raise KeyError
        return needed.value

    def __contains__(self, key: K) -> bool: # type: ignore[override]
        try:
            return True if self[key] is not None else False
        except KeyError:
            return False

    def get_node(self, key: K) -> Optional[Node]:
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
        nodes: List[Node] = []

        def pre_order_traverse(node: Optional[Node]) -> None:
            if node is not None:
                nodes.append(node)
                pre_order_traverse(node.left)
                pre_order_traverse(node.right)

        def post_order_traverse(node: Optional[Node]) -> None:
            if node is not None:
                post_order_traverse(node.left)
                post_order_traverse(node.right)
                nodes.append(node)

        def in_order_traverse(node: Optional[Node]) -> None:
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

    def __setitem__(self, key: K, value: V) -> None:
        if key in self:
            del self[key]

        d1, d2 = split(self, key)
        new_node: Node[K, V] = Node(key, value)
        new_d: Deramida[K, V] = Deramida(new_node)
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


def merge(
    d1: Optional[Deramida], d2: Optional[Deramida]
) -> Deramida:  # all keys in d1 need to be smaller than all key in d2
    def _merge(rt1: Optional[Node], rt2: Optional[Node]) -> Optional[Node]:
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
        return d2 if d2 is not None else Deramida()
    if d2 is None:
        return d1 if d1 is not None else Deramida()
    new_root = _merge(d1.root, d2.root)
    return Deramida(new_root)


def split(
    d: Optional[Deramida], key: K
) -> Tuple[Optional[Deramida], Optional[Deramida]]:  # Left deramida keys < key  |  Right deramida keys > key
    def _split(rt: Optional[Node]) -> Tuple[Optional[Node], Optional[Node]]:
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
