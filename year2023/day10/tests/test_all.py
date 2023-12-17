from pathlib import Path

from utils.file import read_file_line_by_line

from ..main import Day

tests_dir = Path(__file__).parent


def test_part1():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part1 = Day.resolve_part1(input_)
    assert result_part1 == 4, "Part 1 is incorrect"

    input_ = read_file_line_by_line(tests_dir / "test02.txt")
    result_part1 = Day.resolve_part1(input_)
    assert result_part1 == 8, "Part 1 is incorrect"


def test_part2():
    input_ = read_file_line_by_line(tests_dir / "test03.txt")
    result_part2 = Day.resolve_part2(input_)
    assert result_part2 == 4, "Part 2 is incorrect"

    input_ = read_file_line_by_line(tests_dir / "test04.txt")
    result_part2 = Day.resolve_part2(input_)
    assert result_part2 == 8, "Part 2 is incorrect"

    input_ = read_file_line_by_line(tests_dir / "test05.txt")
    result_part2 = Day.resolve_part2(input_)
    assert result_part2 == 10, "Part 2 is incorrect"
