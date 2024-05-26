import pytest

from src.Retest.Retest_1.vector import *


class TestVector:
    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 2]), Vector([3, 3, 3])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0, 0, 0, 0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
            (Vector([11]), Vector([2]), Vector([13])),
        ),
    )
    def test_add(self, vec1, vec2, expected):
        res = vec1 + vec2
        assert res.coords == expected.coords
        assert isinstance(res, Vector)

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 2]), Vector([-1, -1, -1])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0, 0, 0, 0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
            (Vector([11]), Vector([2]), Vector([9])),
        ),
    )
    def test_sub(self, vec1, vec2, expected):
        res = vec1 - vec2
        assert res.coords == expected.coords
        assert isinstance(res, Vector)

    @pytest.mark.parametrize(
        "vec, expected",
        (
            (Vector([1, 1, 1]), 3**0.5),
            (Vector([0, 0, 1, 0, 1, 4]), 18**0.5),
            (Vector([11]), 11),
        ),
    )
    def test_len(self, vec, expected):
        res = vec.len()
        assert res == expected

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 2, 3]), Vector([4, 5, 6]), Vector([-3, 6, -3])),
            (Vector([11, 0, 0]), Vector([0, 0, 2]), Vector([0, -22, 0])),
            (Vector([1, 1, 1]), Vector([1, 1, 1]), Vector([0, 0, 0])),
        ),
    )
    def test_vector_mul(self, vec1, vec2, expected):
        res = vec1.vector_mul(vec2)
        assert res.coords == expected.coords
        assert isinstance(res, Vector)

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 2, 3]), Vector([4, 5, 6]), 32),
            (Vector([11, 0, 0]), Vector([0, 0, 2]), 0),
            (Vector([1, 1, 1]), Vector([1, 1, 1]), 3),
        ),
    )
    def test_scalar_mul(self, vec1, vec2, expected):
        res = vec1.scalar_mul(vec2)
        assert res == expected


class TestExeptionInVector:
    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 24, 4]), Vector([3, 3, 3])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
        ),
    )
    def test_add(self, vec1, vec2, expected):
        with pytest.raises(Exception):
            vec1 + vec2

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 24, 4]), Vector([3, 3, 3])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
        ),
    )
    def test_sub(self, vec1, vec2, expected):
        with pytest.raises(Exception):
            vec1 - vec2

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 24, 4]), Vector([3, 3, 3])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
        ),
    )
    def test_vector_mul(self, vec1, vec2, expected):
        with pytest.raises(Exception):
            vec1.vector_mul(vec2)

    @pytest.mark.parametrize(
        "vec1, vec2, expected",
        (
            (Vector([1, 1, 1]), Vector([2, 2, 24, 4]), Vector([3, 3, 3])),
            (Vector([10, 2222, 1, 3, 1, 4]), Vector([0, 0]), Vector([10, 2222, 1, 3, 1, 4])),
        ),
    )
    def test_scalar_mul(self, vec1, vec2, expected):
        with pytest.raises(Exception):
            vec1.scalar_mul(vec2)
