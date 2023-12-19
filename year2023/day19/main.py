from enum import Enum

from utils.day import AbstractDay
from utils.file import get_sections
from utils.range import get_intersection


class Result(Enum):
    ACCEPTED = "A"
    REJECTED = "R"


def get_workflows(section: list[str]) -> dict[str, dict]:
    workflows = {}
    for line in section:
        name, raw_workflows = line.split("{")
        raw_rules = raw_workflows[:-1].split(",")
        rules = []  # list of (to eval, result if True)
        for i in range(len(raw_rules) - 1):
            rules.append(raw_rules[i].split(":"))
        default = raw_rules[-1]
        workflows[name] = {"rules": rules, "default": default}
    return workflows


def get_parts(section: list[str]) -> list[dict[str, int]]:
    parts = []
    for line in section:
        raw_values = line[1:-1].split(",")
        values = {}
        for raw_value in raw_values:
            part, value = raw_value.split("=")
            values[part] = int(value)
        parts.append(values)
    return parts


def apply_rules(workflow: dict, part_values: list[dict[str, int]], start: str) -> str:
    rules = workflow["rules"]
    for rule in rules:
        to_eval = rule[0]
        part = to_eval[0]
        if (to_eval[1] == "<" and part_values[part] < int(to_eval[2:])) or (
            to_eval[1] == ">" and part_values[part] > int(to_eval[2:])
        ):
            return rule[1]
    return workflow["default"]


def compute_result(
    workflows: dict[str, dict], part: list[dict[str, int]], start: str
) -> Result:
    visited = set()
    result = start
    result_values = {Result.ACCEPTED.value, Result.REJECTED.value}
    while result not in result_values:
        visited.add(result)
        result = apply_rules(workflows[result], part, result)
        if result in visited:
            print("Loop detected")
            return Result.REJECTED
    return Result(result)


def get_range_per_part_for_restriction(
    restrictions: list[str],
) -> dict[str, tuple[int, int]]:
    ranges = {part: (1, 4000) for part in "xmas"}
    for restriction in restrictions:
        operation = [op for op in ["<=", ">=", "<", ">"] if op in restriction][0]
        part, value = restriction.split(operation)
        if operation == "<":
            range_ = (1, int(value) - 1)
        elif operation == ">":
            range_ = (int(value) + 1, 4000)
        elif operation == "<=":
            range_ = (1, int(value))
        elif operation == ">=":
            range_ = (int(value), 4000)

        ranges[part] = get_intersection(ranges[part], range_)
        if ranges[part] is None:
            # impossible path
            return {}

    return ranges


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        worflows_section, part_section = get_sections(lines)
        workflows = get_workflows(worflows_section)
        parts = get_parts(part_section)
        total = 0
        for part in parts:
            result = compute_result(workflows, part, "in")
            if result == Result.ACCEPTED:
                total += sum(part.values())
        return total

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        worflows_section, _ = get_sections(lines)
        workflows = get_workflows(worflows_section)

        def get_unique(
            rules: list[tuple[tuple[str, str, str], str]], default: str
        ) -> tuple[str, str, str]:
            rule = rules[0]
            result_values = {Result.ACCEPTED.value, Result.REJECTED.value}

            return (
                rule[0],
                rule[1]
                if rule[1] in result_values
                else get_unique(
                    workflows[rule[1]]["rules"], workflows[rule[1]]["default"]
                ),
                default
                if (default in result_values and len(rules) == 1)
                else (
                    get_unique(rules[1:], default)
                    if len(rules) > 1
                    else get_unique(
                        workflows[default]["rules"], workflows[default]["default"]
                    )
                ),
            )

        unique: tuple[str, str, str] = get_unique(
            workflows["in"]["rules"], workflows["in"]["default"]
        )

        all_paths = []

        def get_path(
            current_path: list[str],
            to_eval: str,
            if_true: str | tuple,
            otherwise: str | tuple,
        ):
            if if_true == Result.ACCEPTED.value:
                all_paths.append(current_path + [to_eval])
            elif if_true != Result.REJECTED.value:
                get_path(current_path + [to_eval], *if_true)

            opposite_to_eval = (
                to_eval.replace("<", ">=")
                if "<" in to_eval
                else to_eval.replace(">", "<=")
            )
            if otherwise == Result.ACCEPTED.value:
                all_paths.append(current_path + [opposite_to_eval])
            elif otherwise != Result.REJECTED.value:
                get_path(current_path + [opposite_to_eval], *otherwise)

        get_path([], *unique)

        total = 0
        for path in all_paths:
            range_per_part = get_range_per_part_for_restriction(path)
            to_add = 1
            for range in range_per_part.values():
                to_add *= range[1] - range[0] + 1
            total += to_add

        return total
