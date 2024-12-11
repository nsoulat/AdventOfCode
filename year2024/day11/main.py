from collections import Counter
from functools import cache

from utils.day import AbstractDay


@cache
def blink_one_stone(stone: int) -> list[int]:
    stone_str = str(stone)
    if stone == 0:
        return [1]
    if len(stone_str) % 2 == 0:
        return [
            int(stone_str[: len(stone_str) // 2]),
            int(stone_str[len(stone_str) // 2 :]),
        ]
    return [stone * 2024]


def blink(stones: list[int]):
    new_stones = []
    for stone in stones:
        new_stones.extend(blink_one_stone(stone))
    return new_stones


class Day(AbstractDay):

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        stones = list(map(int, lines[0].split(" ")))
        for _ in range(25):
            stones = blink(stones)
        return len(stones)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        stones = list(map(int, lines[0].split(" ")))
        stones_counter = Counter(stones)

        for _ in range(75):
            new_stones_counter = Counter()
            for stone, count in stones_counter.items():
                blinked_stones = blink_one_stone(stone)
                for blinked_stone in blinked_stones:
                    new_stones_counter.update({blinked_stone: count})

            stones_counter = new_stones_counter
        return sum(stones_counter.values())
