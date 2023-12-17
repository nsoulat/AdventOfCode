from itertools import product

from utils.day import AbstractDay
from utils.file import get_sections


def rotate_counterclockwise(section: list[str]) -> list[str]:
    return [
        "".join(section[y][x] for y in range(len(section)))
        for x in range(len(section[0]) - 1, -1, -1)
    ]


def rotate_clockwise(section: list[str]) -> list[str]:
    return [
        "".join(section[y][x] for y in range(len(section) - 1, -1, -1))
        for x in range(len(section[0]))
    ]


def get_length_reflection(part1: list[str], part2: list[str]) -> bool:
    """
    Return the length of the reflected part
    Return 0 if it is not a complete reflection
    """
    max_reflection = 0
    for line1, line2 in zip(part1[::-1], part2):
        if line1 != line2:
            return 0
        max_reflection += 1
    return max_reflection


def find_reflection(
    section: list[str], avoid_line: int | None = None
) -> tuple[tuple[int, int] | None, int]:
    """
    Find the longest horizontal reflection

    Return the left and right indexes, and the length
    """
    best_reflection = None, 0
    for left in range(len(section) - 1):
        if left is avoid_line:
            continue
        right = left + 1
        if (
            length := get_length_reflection(section[:right], section[right:])
        ) > best_reflection[1]:
            best_reflection = (left, right), length
    return best_reflection


def get_best_reflection(
    section: list[str], avoid: tuple[int, bool] | None = None
) -> tuple[int, tuple[int, int], bool]:
    """
    Return the reflection length, the left and right indexes and if it is vertical

    If avoid is specified, it will ignore the line avoid[0]
     for {vertical, horizontal}[avoid[1]] reflection
    """
    horizontal_reflection, horizontal_length = find_reflection(
        section, avoid_line=(avoid[0] if avoid and not avoid[1] else None)
    )
    rotated_section = rotate_clockwise(section)
    vertical_reflection, vertical_length = find_reflection(
        rotated_section, avoid_line=(avoid[0] if avoid and avoid[1] else None)
    )

    is_vertical = vertical_length > horizontal_length
    return (
        (vertical_length, vertical_reflection, True)
        if is_vertical
        else (horizontal_length, horizontal_reflection, False)
    )


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        total = 0
        for section in get_sections(lines):
            _, (left_index, _), is_vertical = get_best_reflection(section)
            total += (left_index + 1) * (1 if is_vertical else 100)
        return total

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        total = 0
        for section in get_sections(lines):
            best_reflection_length, left_length_of_best, is_best_vertical = 0, 0, True

            _, (avoid_line, _), avoid_is_vertical = get_best_reflection(section)
            for x, y in product(range(len(section[0])), range(len(section))):
                modified_section = section.copy()
                modified_section[y] = (
                    modified_section[y][:x]
                    + ("#" if modified_section[y][x] == "." else ".")
                    + modified_section[y][x + 1 :]
                )

                length, reflection_indexes, is_vertical = get_best_reflection(
                    modified_section, avoid=(avoid_line, avoid_is_vertical)
                )
                if length and length > best_reflection_length:
                    best_reflection_length = length
                    left_length_of_best = reflection_indexes[0] + 1
                    is_best_vertical = is_vertical
            total += left_length_of_best * (1 if is_best_vertical else 100)
        return total
