from utils.day import AbstractDay


def get_diff(values: list[int]) -> list[int]:
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def get_previous_and_next_value(values: list[int], diff: list[int]) -> tuple[int, int]:
    if len(diff) == 0:
        raise Exception("Impossible to get full 0")
    if all(d == 0 for d in diff):
        return (values[0], values[-1])
    previous, next = get_previous_and_next_value(diff, get_diff(diff))
    return (values[0] - previous, values[-1] + next)


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        return sum(
            get_previous_and_next_value(line_int, get_diff(line_int))[1]
            for line in lines
            if len(line_int := list(map(int, line.split(" ")))) > 0
        )

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        return sum(
            get_previous_and_next_value(line_int, get_diff(line_int))[0]
            for line in lines
            if len(line_int := list(map(int, line.split(" ")))) > 0
        )
