from pathlib import Path

import pytest

from utils.file import read_file_line_by_line

from ..main import Day

tests_dir = Path(__file__).parent


def test_part1():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part1 = Day.resolve_part1(input_)
    assert result_part1 == 100, "Part 1 is incorrect"


@pytest.mark.skip()
def test_part2():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part2 = Day.resolve_part2(input_)
    assert result_part2 == 25, "Part 2 is incorrect"
