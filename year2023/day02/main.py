from collections import defaultdict
from enum import Enum

from utils.day import AbstractDay


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


MAX_BY_COLOR = {Colors.RED: 12, Colors.GREEN: 13, Colors.BLUE: 14}


def get_count_by_color(reveal: str) -> dict[Colors, int]:
    """
    Parse a reveal and returns the count by colors

    A reveal can be "1 red, 2 green, 6 blue"
    """
    count_by_color = defaultdict(int)
    for draw in reveal.split(", "):
        count, raw_color = draw.split(" ")
        count_by_color[Colors(raw_color)] += int(count)
    return count_by_color


def has_more_than_max(reveals: str) -> bool:
    """
    Return True if and only if there is more
     than MAX allowed for at least one color
     in one of the reveals
    """
    for reveal in reveals.split("; "):
        count_by_color = get_count_by_color(reveal)
        if any(
            [
                count_by_color.get(color, 0) > max_count
                for color, max_count in MAX_BY_COLOR.items()
            ]
        ):
            return True
    return False


def get_max_by_color(reveals: str) -> bool:
    """
    Return the max by each color
     reached in one game
    """
    max_by_color = defaultdict(int)
    for reveal in reveals.split("; "):
        count_by_color = get_count_by_color(reveal)
        for color, count in count_by_color.items():
            max_by_color[color] = max(max_by_color.get(color, 0), count)
    return max_by_color


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        sum_ids = 0
        for line in lines:
            game, reveals = line.split(": ")
            game_id = int(game[len("game ") :])
            if not has_more_than_max(reveals):
                sum_ids += game_id
        return sum_ids

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        sum_powers = 0
        for line in lines:
            _, reveals = line.split(": ")
            max_by_color = get_max_by_color(reveals)
            power = 1
            for color in Colors:
                power *= max_by_color.get(color, 0)
            sum_powers += power
        return sum_powers
