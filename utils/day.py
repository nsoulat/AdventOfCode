from abc import ABC, abstractmethod
from pathlib import Path

from utils.file import read_file_line_by_line


class AbstractDay(ABC):
    """Interface class for each day"""

    @classmethod
    def resolve(cls, input_filepath: Path) -> tuple[int, int]:
        input_ = read_file_line_by_line(input_filepath)
        result_part1 = cls._resolve_part1(lines=input_.copy())
        result_part2 = cls._resolve_part2(lines=input_.copy())
        return result_part1, result_part2

    @classmethod
    @abstractmethod
    def _resolve_part1(cls, lines: list[str]) -> int:
        print("You need to implement Part 1!")
        return None

    @classmethod
    @abstractmethod
    def _resolve_part2(cls, lines: list[str]) -> int:
        print("You need to implement Part 2!")
        return None
