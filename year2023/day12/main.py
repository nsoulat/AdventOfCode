from functools import cache

from utils.day import AbstractDay


def count_possibility(lines: list[str], unfold: int = 1) -> int:
    @cache
    def get_possibilities_for_line(
        end_line: str, raw_expected_damaged: str, last_pos=""
    ):
        if not raw_expected_damaged:
            return "#" not in end_line
        expected_damaged = list(map(int, raw_expected_damaged.split(",")))
        begin = 0
        while begin < len(end_line) and end_line[begin] == ".":
            last_pos = "."
            begin += 1
        end_line = end_line[begin:]
        if not end_line:
            return 0
        dot_try, hash_try = 0, 0
        if end_line[0] == "?":
            # try "."
            dot_try = get_possibilities_for_line(
                end_line[1:], ",".join(map(str, expected_damaged)), "."
            )
            # try "#"
            if (last_pos != "#") and ("." not in end_line[: expected_damaged[0]]):
                if len(end_line) > expected_damaged[0]:
                    if end_line[expected_damaged[0]] != "#":
                        # add the gap "."
                        hash_try = get_possibilities_for_line(
                            end_line[expected_damaged[0] + 1 :],
                            ",".join(map(str, expected_damaged[1:])),
                            ".",
                        )
                elif len(end_line) == expected_damaged[0]:
                    hash_try = get_possibilities_for_line(
                        end_line[expected_damaged[0] :],
                        ",".join(map(str, expected_damaged[1:])),
                        "#",
                    )

        elif end_line[0] == "#":
            if "." in end_line[: expected_damaged[0]]:
                return 0
            if len(end_line) < expected_damaged[0] or (
                len(end_line) > expected_damaged[0]
                and end_line[expected_damaged[0]] == "#"
            ):
                # impossible as they aren't enough characters remaining
                # or there is a missing gap between two damaged parts
                return 0
            hash_try = get_possibilities_for_line(
                end_line[expected_damaged[0] :],
                ",".join(map(str, expected_damaged[1:])),
                "#",
            )
        return dot_try + hash_try

    line_ = 0
    all_count = []
    for raw_line in lines:
        line_ += 1
        line, raw_expected_damaged = raw_line.split(" ")
        line = "?".join(line for _ in range(unfold))
        raw_expected_damaged = ",".join(raw_expected_damaged for _ in range(unfold))

        all_count.append(get_possibilities_for_line(line, raw_expected_damaged))
    return sum(all_count)


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        return count_possibility(lines)

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        return count_possibility(lines, unfold=5)
