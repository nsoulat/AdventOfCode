from pathlib import Path

from utils.file import read_file_line_by_line

from ..main import Day

tests_dir = Path(__file__).parent


def test_part_1():
    result_part1 = Day._resolve_part1(read_file_line_by_line(tests_dir / "test01.txt"))
    assert result_part1 == 2, "Part 1 is incorrect"

    result_part1 = Day._resolve_part1(read_file_line_by_line(tests_dir / "test02.txt"))
    assert result_part1 == 6, "Part 1 is incorrect"


def test_part_2():
    result_part2 = Day._resolve_part2(read_file_line_by_line(tests_dir / "test03.txt"))
    assert result_part2 == 6, "Part 2 is incorrect"
