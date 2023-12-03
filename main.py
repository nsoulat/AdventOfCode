from datetime import datetime
from importlib import import_module
from pathlib import Path

import click

from utils.day import AbstractDay


@click.command()
@click.option("-d", "--day", type=int, required=False)
@click.option("-y", "--year", type=int, required=False)
@click.option("-i", "--input", "input_file", required=False, type=str)
def get_solution(
    day: int | None = None,
    year: int | None = None,
    input_file: str | None = None,
):
    now = datetime.now()
    day = day or now.day
    year = year or now.year

    # add a leading 0 until day is 2-character width
    # https://docs.python.org/3/library/string.html#format-examples
    target_dir_path = f"year{year}/day{day:02d}"
    target_dir = Path(target_dir_path)
    if not target_dir.exists():
        click.echo("The target directory doesn't exist")
        raise SystemExit(1)

    day_module = import_module(f"{target_dir_path.replace("/", ".")}.main")
    day_kls: AbstractDay = getattr(day_module, "Day")

    input_filepath = Path(input_file) if input_file else (target_dir / "input.txt")
    if not input_filepath.exists():
        click.echo(
            (
                f"The input file ({input_filepath}) does not exist."
                " Add the 'input.txt' file or use '-i <input_filepath>'"
            )
        )
        raise SystemExit(1)

    result_part1, result_part2 = day_kls.resolve(input_filepath)

    click.echo((
        f"result for day {day} (year {year}) ->"
        f" part1: {result_part1}, part2: {result_part2}"
    ))


if __name__ == "__main__":
    get_solution()
