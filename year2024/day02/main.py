from collections import Counter, defaultdict

from utils.day import AbstractDay


def is_report_safe(levels: list[int], try_remove_one_level: bool = False) -> bool:
    is_increasing = levels[0] < levels[1]
    multiplier = 2 * int(is_increasing) - 1  # 1 if increasing, -1 if decreasing
    for i in range(len(levels) - 1):
        if not (1 <= multiplier * (levels[i + 1] - levels[i]) <= 3):
            return (
                (
                    any(
                        is_report_safe(levels[:j] + levels[j + 1 :])
                        for j in range(len(levels))
                    )
                )
                if try_remove_one_level
                else False
            )
    return True


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        safe_reports_count = 0
        for line in lines:
            levels = list(map(int, line.split(" ")))
            if is_report_safe(levels):
                safe_reports_count += 1
        return safe_reports_count

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        safe_reports_count = 0
        for line in lines:
            levels = list(map(int, line.split(" ")))
            if is_report_safe(levels, try_remove_one_level=True):
                safe_reports_count += 1
        return safe_reports_count
