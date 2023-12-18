from utils.day import AbstractDay


def compute_area(steps: list[tuple[str, int]]) -> int:
    """
    Compute the area of a Freeman chain code

    see https://en.wikipedia.org/wiki/Chain_code
    and https://en.wikipedia.org/wiki/Pick's_theorem
    """
    # place ourself in coordinates with +x is down and +y is right
    # so going first right will give a counterclockwise perimeter
    enclosed_area = 0
    perimeter = 0
    yposition = 0
    for direction, length in steps:
        perimeter += length
        if direction == "U":
            enclosed_area -= length * yposition
        elif direction == "D":
            enclosed_area += length * yposition
        elif direction == "R":
            yposition += length
        elif direction == "L":
            yposition -= length
    return enclosed_area + perimeter // 2 + 1


def get_steps(lines: list[str]) -> list[tuple[str, int]]:
    steps = []
    dir_digit = ["R", "D", "L", "U"]
    for line in lines:
        hexa_instruction = line.split(" ")[2][2:-1]  # remove parenthesis and hastag
        length = int(hexa_instruction[:5], 16)
        direction = dir_digit[int(hexa_instruction[5])]
        steps.append((direction, int(length)))
    return steps


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return compute_area(
            [(x[0], int(x[1])) for line in lines if (x := line.split(" "))]
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return compute_area(get_steps(lines))
