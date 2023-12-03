from pathlib import Path


def read_file_line_by_line(filepath: Path) -> list[str]:
    with open(filepath, "r") as file:
        input_ = [line.rstrip() for line in file.readlines()]
    return input_
