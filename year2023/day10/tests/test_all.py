from pathlib import Path

from ..main import Day

tests_dir = Path(__file__).parent


def test_part_1():
    result_part1, _ = Day.resolve(tests_dir / "test01.txt")
    assert result_part1 == 4, "Part 1 is incorrect"

    result_part1, _ = Day.resolve(tests_dir / "test02.txt")
    assert result_part1 == 8, "Part 1 is incorrect"


def test_part_2():
    _, result_part2 = Day.resolve(tests_dir / "test03.txt")
    assert result_part2 == 4, "Part 2 is incorrect"

    _, result_part2 = Day.resolve(tests_dir / "test04.txt")
    assert result_part2 == 8, "Part 2 is incorrect"

    _, result_part2 = Day.resolve(tests_dir / "test05.txt")
    assert result_part2 == 10, "Part 2 is incorrect"
