from utils.day import AbstractDay


def run_HASH(string: str) -> int:
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        steps: list[str] = lines[0].split(",")
        return sum(run_HASH(step) for step in steps)

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        steps: list[str] = lines[0].split(",")
        lens_by_box = {box: {"lens": [], "fc_by_label": {}} for box in range(256)}
        for step in steps:
            operation = "=" if "=" in step else "-"
            label, focal_length = step.split(operation)
            box = run_HASH(label)
            if operation == "-":
                if label in lens_by_box[box]["fc_by_label"]:
                    lens_by_box[box]["lens"].remove(label)
                    del lens_by_box[box]["fc_by_label"][label]
            else:
                if label not in lens_by_box[box]["fc_by_label"]:
                    lens_by_box[box]["lens"].append(label)
                    lens_by_box[box]["fc_by_label"][label] = focal_length

                else:
                    lens_by_box[box]["fc_by_label"][label] = focal_length

        return sum(
            (box + 1) * slot * int(lens_by_box[box]["fc_by_label"][label])
            for box, items in lens_by_box.items()
            for slot, label in enumerate(items["lens"], 1)
        )
