from utils.range import (
    get_distinct_by,
    get_exclusive_union,
    get_global_union,
    get_intersection,
)


def test_get_intersection():
    assert get_intersection((0, 2), (1, 3)) == (1, 2)
    assert get_intersection((1, 3), (0, 2)) == (1, 2)
    assert get_intersection((1, 3), (1, 4)) == (1, 3)
    assert get_intersection((1, 3), (0, 3)) == (1, 3)
    assert get_intersection((2, 4), (2, 4)) == (2, 4)
    assert get_intersection((0, 2), (2, 4)) == (2, 2)
    assert get_intersection((0, 1), (2, 4)) is None


def test_get_global_union():
    assert get_global_union((0, 2), (1, 3)) == (0, 3)
    assert get_global_union((1, 3), (0, 2)) == (0, 3)
    assert get_global_union((1, 3), (1, 4)) == (1, 4)
    assert get_global_union((1, 3), (0, 3)) == (0, 3)
    assert get_global_union((2, 4), (2, 4)) == (2, 4)
    assert get_global_union((0, 2), (2, 4)) == (0, 4)
    assert get_global_union((0, 1), (2, 4)) == (0, 4)


def test_get_exclusion_union():
    assert get_exclusive_union((0, 2), (1, 3)) == ((0, 1), (2, 3))
    assert get_exclusive_union((1, 3), (0, 2)) == ((0, 1), (2, 3))
    assert get_exclusive_union((1, 3), (1, 4)) == (None, (3, 4))
    assert get_exclusive_union((1, 3), (0, 3)) == ((0, 1), None)
    assert get_exclusive_union((2, 4), (2, 4)) == (None, None)
    assert get_exclusive_union((0, 2), (2, 4)) == ((0, 2), (2, 4))
    assert get_exclusive_union((0, 1), (2, 4)) == ((0, 1), (2, 4))


def test_get_distinct_by():
    initial_ranges = [(-3, -1), (0, 5), (8, 10)]

    assert get_distinct_by(initial_ranges, []) == initial_ranges
    assert get_distinct_by(initial_ranges, [(6, 7)]) == initial_ranges
    assert get_distinct_by(initial_ranges, [(-10, -8), (11, 12)]) == initial_ranges
    assert get_distinct_by(initial_ranges, [(1, 1)]) == (
        [
            (-3, -1),
            (0, 0),
            (1, 1),
            (2, 5),
            (8, 10),
        ]
    )
    assert get_distinct_by(initial_ranges, [(-2, 2), (9, 11)]) == (
        [
            (-3, -3),
            (-2, -1),
            (0, 2),
            (3, 5),
            (8, 8),
            (9, 10),
        ]
    )
    assert get_distinct_by(initial_ranges, [(2, 3)]) == (
        [
            (-3, -1),
            (0, 1),
            (2, 3),
            (4, 5),
            (8, 10),
        ]
    )
