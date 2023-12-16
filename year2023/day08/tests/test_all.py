from pathlib import Path

from ..main import Day

tests_dir = Path(__file__).parent


def test_part_1():
    result_part1, _ = Day.resolve(tests_dir / "test01.txt")
    assert result_part1 == 2, "Part 1 is incorrect"

    result_part1, _ = Day.resolve(tests_dir / "test02.txt")
    assert result_part1 == 6, "Part 1 is incorrect"


def test_part_2():
    _, result_part2 = Day.resolve(tests_dir / "test03.txt")
    assert result_part2 == 6, "Part 2 is incorrect"
