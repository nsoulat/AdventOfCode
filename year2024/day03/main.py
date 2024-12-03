import re

from utils.day import AbstractDay


def extract_and_count_for_line(line: str):
    matches = re.findall(r"mul\((\d+),(\d+)\)", line)  # capture integers
    return sum(int(x) * int(y) for x, y in matches)


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return sum(extract_and_count_for_line(line) for line in lines)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        do_split = [split.split("don't()")[0] for split in "".join(lines).split("do()")]
        # each beginning split is in 'enabled' mode, and the rest is in 'disabled' mode

        return sum(extract_and_count_for_line(split) for split in do_split)
