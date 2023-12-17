from abc import ABC, abstractmethod


class AbstractDay(ABC):
    """Interface class for each day"""

    @classmethod
    @abstractmethod
    def resolve_part1(cls, lines: list[str]) -> int:
        print("You need to implement Part 1!")
        return None

    @classmethod
    @abstractmethod
    def resolve_part2(cls, lines: list[str]) -> int:
        print("You need to implement Part 2!")
        return None
