from pathlib import Path

from ..main import Day

tests_dir = Path(__file__).parent


def test_day():
    result_part1, result_part2 = Day.resolve(tests_dir / "test01.txt")
    assert result_part1 == 114, "Part 1 is incorrect"
    assert result_part2 == 2, "Part 2 is incorrect"
