from utils.day import AbstractDay
from utils.file import get_sections


def get_minimum(ordering_rules: set[tuple[int, int]]) -> int:
    # the minimum is the only one that is not in the second part
    left_ones, right_ones = zip(*ordering_rules)
    minimal_ones = set(left_ones) - set(right_ones)
    if len(minimal_ones) != 1:
        print(minimal_ones)
        print(ordering_rules)
        raise ValueError("There is no minimum or more than one!")
    return list(minimal_ones)[0]


class Day(AbstractDay):
    @classmethod
    def _resolve(
        cls,
        lines: list[str],
        only_correctly_sorted: bool = False,
        only_incorrectly_sorted: bool = False,
    ):
        raw_ordering_rules, raw_updates = get_sections(lines)
        ordering_rules = [
            (int(x[0]), int(x[1]))
            for x in [line.split("|") for line in raw_ordering_rules]
        ]

        updates = [list(map(int, raw_update.split(","))) for raw_update in raw_updates]
        sum_middle = 0
        for update in updates:

            order: dict[int, int] = {}  # order index for each page
            order_index = 0
            numbers_in_update = set(update)
            ordering_rule_for_update = {
                ordering_rule
                for ordering_rule in ordering_rules
                if (
                    ordering_rule[0] in numbers_in_update
                    and ordering_rule[1] in numbers_in_update
                )
            }

            while numbers_in_update:
                if len(numbers_in_update) == 1:
                    minimum = list(numbers_in_update)[0]
                else:
                    minimum = get_minimum(ordering_rule_for_update)
                order[minimum] = order_index
                order_index += 1
                numbers_in_update.remove(minimum)
                ordering_rule_for_update = {
                    ordering_rule
                    for ordering_rule in ordering_rule_for_update
                    if ordering_rule[0] != minimum
                }

            sorted_update = sorted(update, key=lambda x: order[x])
            is_correctly_sorted = sorted_update == update
            if only_correctly_sorted and is_correctly_sorted:
                sum_middle += sorted_update[len(update) // 2]
            elif only_incorrectly_sorted and not is_correctly_sorted:
                sum_middle += sorted_update[len(update) // 2]
        return sum_middle

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return cls._resolve(lines, only_correctly_sorted=True)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return cls._resolve(lines, only_incorrectly_sorted=True)
