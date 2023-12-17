from functools import reduce

from utils.day import AbstractDay
from utils.equation import solve_equation_degree_2


def get_record_distances_per_time(lines: list[str], _version=1) -> dict[int, int]:
    times_raw = lines[0][len("Time: ") :]
    distances_raw = lines[1][len("Distance: ") :]
    if _version == 2:
        times = [int(times_raw.replace(" ", ""))]
        distances = [int(distances_raw.replace(" ", ""))]
    else:
        times = list(map(int, [time for time in times_raw.split(" ") if time != ""]))
        distances = list(
            map(int, [dist for dist in distances_raw.split(" ") if dist != ""])
        )
    return {time: distance for time, distance in zip(times, distances)}


def get_range_time_for_better_distance(time: int, record: int) -> tuple[int, int]:
    """
    Return the range (inclusive) of all button holding times that
    gives a better distance (strictly)
    """
    # with D record for time T, holding we want the button holding time t
    # to be such as (T-t)*t > D as (T-t) is the total time going forward,
    # at speed t/1ms
    # Thus we have an 2nd degree inequation
    float_t1, float_t2 = solve_equation_degree_2(1, -time, record)
    # a=1 > 0 so we have float_t1 < solutions < float_t2 (to a strict better time)

    t1, t2 = int(float_t1), int(float_t2)
    # we want inclusive range so we check if t1 and t2 are solutions
    t1 = (
        t1
        if compute_distance(get_speed_per_time_hold(t1), time - t1) > record
        else t1 + 1
    )
    t2 = (
        t2
        if compute_distance(get_speed_per_time_hold(t2), time - t2) > record
        else t2 - 1
    )

    return t1, t2


def get_speed_per_time_hold(time: int) -> int:
    return time


def compute_distance(speed: int, time: int) -> int:
    return speed * time


class Day(AbstractDay):
    @classmethod
    def _resolve(cls, lines: list[str], version=1):
        count_possibility = []
        for time, record in get_record_distances_per_time(
            lines, _version=version
        ).items():
            t1, t2 = get_range_time_for_better_distance(time, record)
            count_possibility.append(t2 - t1 + 1)
        return reduce(lambda x, y: x * y, count_possibility)

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return cls._resolve(lines, version=1)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return cls._resolve(lines, version=2)
