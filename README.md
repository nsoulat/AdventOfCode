# Advent of code

<https://adventofcode.com>

## Install the project

The project uses `Python 3.12` and [pdm](https://pdm-project.org/latest/) as Python package manager.

To install all the packages, use:

```sh
pdm install
```

## To get result from a specific day

```sh
pdm run main.py -d <day: int> -y <year: int> -i <input_filepath>
```

If `day` is not given, current `day` will be used. Same for `year`.

If `input_filepath` is not given, the `input.txt` file in the year/day folder will be used (it is the default file created when automatically creating a new day folder)

## To add the template for a new day [NOT YET AVAILABLE]

This will automatically create a new folder for the day.

If `ADVENT_SESSION_ID` and `ADVENT_USER_AGENT` are set up, it will also fetch the input for the day and add it to `input.txt`

### For today (day and year automatic)

```sh
pdm run main.py new
```

### For a specific day and year

```sh
pdm run main.py new -d <day: int> -y <year: int>
```

## To run tests

```sh
pdm run pytest
```
