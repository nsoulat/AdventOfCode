import os

import requests

ADVENT_URL = "http://adventofcode.com/{year}/day/{day}"
ADVENT_URL_INPUT = f"{ADVENT_URL}/input"
SESSION_ID = os.getenv("ADVENT_SESSION_ID")
USER_AGENT = os.getenv("ADVENT_USER_AGENT")


def get_input(day: int, year: int):
    uri = ADVENT_URL_INPUT.format(year=year, day=day)
    return requests.get(
        uri, cookies={"session": SESSION_ID}, headers={"User-Agent": USER_AGENT}
    )
