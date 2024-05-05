from random import randint
from typing import Any, Generic, List, MutableMapping, Optional, Tuple, TypeVar, Union

K = TypeVar("K")
V = TypeVar("V")


class PrinterMixin:
    root: "Optional[Node]"  # to avoid mypy error: [attr-defined]

    def __str__(self) -> str:
        def _get_lines(node: Optional[Node], string: str, level: int = 0) -> str:
            if node is not None:
                string = _get_lines(node.left, string, level + 1)
                indent_by_depth = " " * 4 * level
                string += f"Depth: {level} {indent_by_depth}|---> ({node.priority}, {node.key})\n"
                string += _get_lines(node.right, string, level + 1)
                return string
            else:
                return ""

        return _get_lines(self.root, "")

    def __repr__(self) -> str:
        def _get_nodes(curr_root: Union[Node, Any]) -> str:
            if curr_root.left is None and curr_root.right is None:
                return f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, left=None, right=None)"
            curr_repr = f"Node(priority={curr_root.priority}, key={curr_root.key}, value={curr_root.value}, "
            curr_repr += f"left={_get_nodes(curr_root.left)}, " if curr_root.left is not None else "left=None, "
            curr_repr += f"right={_get_nodes(curr_root.right)})" if curr_root.right is not None else "right=None)"
            return curr_repr

        return _get_nodes(self.root)


class Node(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.priority: int = randint(0, int(1e9))
        self.key: K = key
        self.value: V = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __str__(self) -> str:
        return f"priority={self.priority}, key={self.key}, value={self.value}"

    def __lt__(self, other: "Node") -> bool:
        if self.priority > other.priority:
            return False
        elif self.priority < other.priority:
            return True
        else:
            return self.key < other.key

    def __eq__(self, other: "Node") -> bool:  # type: ignore[override]
        return self.priority == other.priority and self.key == other.key


class Treap(MutableMapping, PrinterMixin, Generic[K, V]):
    def __init__(self, node: Optional[Node] = None) -> None:
        self.root: Optional[Node] = node
        self.len = 1 if node else 0

    def __getitem__(self, key: K) -> V:
        needed = self.get_node(key)
        if needed is None or needed.key != key:
            raise KeyError
        return needed.value

    def __contains__(self, key: K) -> bool:  # type: ignore[override]
        return self.get_node(key) is not None

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

        rt1, rt2 = Treap.split(key, self.root)
        new_node: Node[K, V] = Node(key, value)
        rt2 = Treap.merge(new_node, rt2)
        self.root = Treap.merge(rt1, rt2)
        self.len += 1

    def __delitem__(self, key: K) -> None:
        deleting = self.get_node(key)
        if deleting is None:
            raise KeyError(f"There is no {key} in Treap")
        rt1, rt2 = Treap.split(key, self.root)
        del deleting
        self.root = Treap.merge(rt1, rt2)
        self.len -= 1

    def __iter__(self) -> Any:
        nodes = self.traverse()
        for node in nodes:
            yield node

    def __len__(self) -> int:
        return self.len

    @staticmethod
    def merge(node1: Optional[Node], node2: Optional[Node]) -> Optional[Node]:
        if node1 is None:
            return node2
        if node2 is None:
            return node1
        if node1.priority > node2.priority:
            node1.right = Treap.merge(node1.right, node2)
            return node1
        else:
            node2.left = Treap.merge(node1, node2.left)
            return node2

    @staticmethod
    def split(key: Any, rt: Optional[Node]) -> Tuple[Optional[Node], Optional[Node]]:
        if rt is None:
            return None, None
        if rt.key < key:
            d1_rt, d2_rt = Treap.split(key, rt.right)
            rt.right = d1_rt
            return rt, d2_rt
        elif rt.key > key:
            d1_rt, d2_rt = Treap.split(key, rt.left)
            rt.left = d2_rt
            return d1_rt, rt
        return rt.left, rt.right
