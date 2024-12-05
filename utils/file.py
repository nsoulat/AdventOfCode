from pathlib import Path


def read_file_line_by_line(filepath: Path) -> list[str]:
    with open(filepath, "r") as file:
        input_ = [line.rstrip() for line in file.readlines()]
    return input_


def get_sections(lines: list[str]) -> list[list[str]]:
    sections: list[list[str]] = []
    add_to_section = []
    for i, line in enumerate(lines):
        if not line:
            continue
        add_to_section.append(line)
        if i == len(lines) - 1 or lines[i + 1] == "":
            sections.append(add_to_section)
            add_to_section = []
    return sections
