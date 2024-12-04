from utils.day import AbstractDay


def is_x_mas(lines: list[str], h: int, w: int) -> bool:
    return (
        1 <= h <= len(lines) - 2
        and 1 <= w <= len(lines[0]) - 2
        and (
            lines[h][w] == "A"
            and (
                (lines[h - 1][w - 1] + lines[h + 1][w + 1]) in ("SM", "MS")
                and (lines[h - 1][w + 1] + lines[h + 1][w - 1]) in ("SM", "MS")
            )
        )
    )


def count_xmas_in_line(lines: list[str]) -> int:
    return sum(line.count("XMAS") + line.count("SAMX") for line in lines)


def get_vertical(lines: list[str]) -> list[str]:
    width = len(lines[0])
    return ["".join(line[i] for line in lines) for i in range(width)]


def get_diagonal_one(lines: list[str]) -> list[str]:
    """top left to bottom right diagonal"""
    width = len(lines[0])
    height = len(lines)
    res = []
    for h in range(-width + 1, height):
        h, width_offset = (
            (0, -h) if h < 0 else (h, 0)
        )  # it means that we begin the diagonal at [0, h] instead of [h, 0]
        new_line = ""
        for i in range(min(height - h, width - width_offset)):
            new_line += lines[h + i][i + width_offset]
        res.append(new_line)
    return res


def diagonal_two(lines: list[str]) -> list[str]:
    return get_diagonal_one([line[::-1] for line in lines])


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        special_lines = [
            lines,
            get_vertical(lines),
            get_diagonal_one(lines),
            diagonal_two(lines),
        ]
        return sum(count_xmas_in_line(special_lines) for special_lines in special_lines)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return sum(
            is_x_mas(lines, h, w)
            for w in range(len(lines[0]))
            for h in range(len(lines))
        )
