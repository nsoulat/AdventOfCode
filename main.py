from datetime import datetime
from importlib import import_module
from pathlib import Path
from time import perf_counter

import click

from utils.day import AbstractDay
from utils.file import read_file_line_by_line


def timeit(fun, *args, **kwargs):
    t0 = perf_counter()
    output = fun(*args, **kwargs)
    t1 = perf_counter()
    return (output, t1 - t0)


@click.command()
@click.option("-d", "--day", type=int, required=False)
@click.option("-y", "--year", type=int, required=False)
@click.option("-i", "--input", "input_file", required=False, type=str)
@click.option("--timer", required=False, is_flag=True)
def get_solution(
    day: int | None, year: int | None, input_file: str | None, timer: bool
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

    day_module = import_module(f"{target_dir_path.replace('/', '.')}.main")
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

    input_ = read_file_line_by_line(input_filepath)
    result_part1, elapsed_time_part1 = timeit(
        day_kls.resolve_part1, lines=input_.copy()
    )
    result_part2, elapsed_time_part2 = timeit(
        day_kls.resolve_part2, lines=input_.copy()
    )

    timing_part1 = "" if not timer else f"({elapsed_time_part1}s)"
    timing_part2 = "" if not timer else f"({elapsed_time_part2}s)"

    click.echo(
        (
            f"result for day {day} (year {year}):"
            f"\n part1: {result_part1} {timing_part1}"
            f"\n part2: {result_part2} {timing_part2}"
        )
    )


if __name__ == "__main__":
    get_solution()
