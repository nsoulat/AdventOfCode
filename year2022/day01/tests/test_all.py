from pathlib import Path

from utils.file import read_file_line_by_line

from ..main import Day


def test_01():
    _input = read_file_line_by_line(Path("year2022/day01/tests/test01.txt"))
    assert Day._resolve(_input) == 100


def test_02():
    _input = read_file_line_by_line(Path("year2022/day01/tests/test02.txt"))
    assert Day._resolve(_input) == 25
