from collections import Counter, defaultdict

from utils.day import AbstractDay


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        left_locations, right_locations = [], []
        for line in lines:
            left_location, right_location = map(int, line.split("   "))
            left_locations.append(left_location)
            right_locations.append(right_location)
        left_locations.sort()
        right_locations.sort()
        return sum(
            abs(left - right) for left, right in zip(left_locations, right_locations)
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        left_locations, right_locations_count = [], defaultdict(int)
        for line in lines:
            left_location, right_location = map(int, line.split("   "))
            left_locations.append(left_location)
            right_locations_count[right_location] += 1

        return sum(left * right_locations_count[left] for left in left_locations)
