from typing import Any, Generic, TypeVar


class ArithmeticAvailable:
    def __add__(self, other: Any) -> Any:
        raise NotImplementedError

    def __sub__(self, other: Any) -> Any:
        raise NotImplementedError

    def __mul__(self, other: Any) -> Any:
        raise NotImplementedError


T = TypeVar("T", bound=ArithmeticAvailable)


class Vector(Generic[T]):
    def __init__(self, coords: list[T]) -> None:
        self.coords: list[T] = coords

    def __add__(self, other: "Vector") -> "Vector":
        if len(self.coords) != len(other.coords):
            raise Exception("dimensions should be equals")
        return Vector([self.coords[i] + other.coords[i] for i in range(len(self.coords))])

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self.coords) != len(other.coords):
            raise Exception("dimensions should be equals")
        return Vector([self.coords[i] - other.coords[i] for i in range(len(self.coords))])

    def __str__(self) -> str:
        return "Vector(" + ",".join([str(x) for x in self.coords]) + ")"

    def len(self) -> T:
        return sum([x * x for x in self.coords]) ** 0.5

    def vector_mul(self, other: "Vector") -> "Vector":
        if len(self.coords) != 3 or len(other.coords) != 3:
            raise Exception("dimensions should be equals")
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords
        x3 = y1 * z2 - z1 * y2
        y3 = z1 * x2 - x1 * z2
        z3 = x1 * y2 - y1 * x2
        return Vector([x3, y3, z3])

    def scalar_mul(self, other: "Vector") -> int:
        if len(self.coords) != len(other.coords):
            raise Exception("dimensions should be equals")
        return sum(self.coords[i] * other.coords[i] for i in range(len(self.coords)))

    def is_null(self) -> bool:
        for i in self.coords:
            if i != 0:
                return False
        return True
