from utils.day import AbstractDay


def parse_line(line: str) -> tuple[int, list[int]]:
    total, raw_numbers = line.split(": ")
    numbers = list(map(int, raw_numbers.split(" ")))
    return int(total), numbers


def is_total_possible(total: int, numbers: list[int], with_concatenation: bool) -> bool:
    first_value, *rest_values = numbers
    possible_values = {first_value}
    for number in rest_values:
        possible_values: set[int] = {
            *(
                new_value
                for value in possible_values
                if (new_value := value * number) <= total
            ),
            *(
                new_value
                for value in possible_values
                if (new_value := value + number) <= total
            ),
            *(
                (
                    new_value
                    for value in possible_values
                    if (new_value := int(f"{value}{number}")) <= total
                )
                if with_concatenation
                else []
            ),
        }
    return total in possible_values


class Day(AbstractDay):
    @classmethod
    def _resolve(cls, lines: list[str], with_concatenation: bool):
        res = 0
        for line in lines:
            total, numbers = parse_line(line)
            if is_total_possible(total, numbers, with_concatenation):
                res += total
        return res

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return cls._resolve(lines, with_concatenation=False)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return cls._resolve(lines, with_concatenation=True)
