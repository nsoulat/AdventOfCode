from utils.day import AbstractDay


class Day(AbstractDay):
    @classmethod
    def _resolve(cls, lines: list[str]):
        total_by_elves = [0]
        for cal in lines:
            if not cal or cal == "\n":
                total_by_elves.append(0)
            else:
                total_by_elves[-1] += int(cal)
        return max(total_by_elves)

    @classmethod
    def resolve_part1(cls, lines: list[str]) -> int:
        return cls._resolve(lines)

    @classmethod
    def resolve_part2(cls, lines: list[str]) -> int:
        return cls._resolve(lines)
