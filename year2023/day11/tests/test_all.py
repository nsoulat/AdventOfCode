from pathlib import Path

from utils.file import read_file_line_by_line

from ..main import Day

tests_dir = Path(__file__).parent


def test_part1():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part1 = Day.resolve_part1(input_)
    assert result_part1 == 374, "Part 1 is incorrect"


def test_part2():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    assert Day._resolve(input_, expand_thickness=9) == 1030, "Part 2 is incorrect"
    assert Day._resolve(input_, expand_thickness=99) == 8410, "Part 2 is incorrect"
