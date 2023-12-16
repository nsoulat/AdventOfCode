from utils.day import AbstractDay
from utils.file import get_sections
from utils.range import get_distinct_by


def get_map_from_section(
    section: list[str],
) -> tuple[str, str, dict[tuple[int, int], int]]:
    """
    Assuming the first line is the conversion map head
    and the following the conversion map

    Returns the source, destination and the map which is a dict that for
     a given (source_start, source_end) pair (both inclusive) gives the difference to
     add to the source number to get the destination number
    """
    first_line = section[0]
    maps_raw = first_line[: len(first_line) - len("map: ")]
    source, destination = maps_raw.split("-to-")

    map_: dict[int, int] = {}
    for line in section[1:]:
        destination_start, source_start, range_ = list(map(int, line.split(" ")))
        map_[(source_start, source_start + range_ - 1)] = (
            destination_start - source_start
        )

    return (source, destination, map_)


def get_seeds(section: list[str]) -> int:
    first_line_value = section[0][len("seeds: ") :]
    return list(map(int, first_line_value.split(" ")))


def get_seeds_by_range(section: list[str]) -> list[tuple[int, int]]:
    values = get_seeds(section)
    seeds = []
    for i in range(0, len(values), 2):
        seed_start, seed_end = values[i], values[i] + values[i + 1]
        seeds.append((seed_start, seed_end))
    return seeds


def get_conversion_order_and_maps(
    sections: list[str],
) -> tuple[list[str], dict[(str, str), dict[tuple[int, int], int]]]:
    """
    Return the conversion order and the conversion map
     ie. a dict that for each (source_category, destination_category) pair
     returns a dict that gives the destination_number for a given source_number

    If the given source_number is not in the dict,
     assume destination_number = source_number
    """
    conversion_map = {}
    conversion_order = []
    for section in sections:
        source, destination, map_ = get_map_from_section(section)
        conversion_map[(source, destination)] = map_
        conversion_order.append((source, destination))

    return conversion_order, conversion_map


def get_destination_number(
    conversion_map: dict[(str, str), dict[int, int]],
    source_category: str,
    source_number: int,
    destination_category: str,
) -> int:
    map_ = conversion_map[(source_category, destination_category)]
    for (source_start, source_end), difference_to_add in map_.items():
        if source_start <= source_number <= source_end:  # source_end is included
            return source_number + difference_to_add
    return source_number


def get_destination_range_per_range_seeds(
    conversion_map: dict[(str, str), dict[int, int]],
    seed_range: tuple[int, int],
    source_category: str,
    source_range: tuple[int, int],
    destination_category: str,
) -> dict[tuple[int, int], tuple[int, int]]:
    map_ = conversion_map[(source_category, destination_category)]
    new_source_ranges = get_distinct_by([source_range], list(map_.keys()))
    return {
        (
            seed_range[0] + new_source_start - source_range[0],
            seed_range[1] - new_source_end + source_range[1],
        ): (
            get_destination_number(
                conversion_map,
                source_category,
                new_source_start,
                destination_category,
            ),
            get_destination_number(
                conversion_map,
                source_category,
                new_source_end,
                destination_category,
            ),
        )
        for new_source_start, new_source_end in new_source_ranges
    }


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        sections = get_sections(lines)
        seeds = get_seeds(sections.pop(0))
        conversion_order, conversion_map = get_conversion_order_and_maps(sections)
        location_per_seed = {}
        for seed in seeds:
            value = seed
            for source_category, destination_category in conversion_order:
                value = get_destination_number(
                    conversion_map=conversion_map,
                    source_category=source_category,
                    source_number=value,
                    destination_category=destination_category,
                )
            location_per_seed[seed] = value

        return min(location_per_seed.values())

    @classmethod
    def _resolve_part2_naif(cls, lines: list[str]):
        sections = get_sections(lines)
        seed_ranges = get_seeds_by_range(sections.pop(0))
        seeds = []
        for seed_start, seed_end in seed_ranges:
            for seed in range(seed_start, seed_end + 1):
                seeds.append(seed)
        conversion_order, conversion_map = get_conversion_order_and_maps(sections)
        location_per_seed = {}
        for seed in seeds:
            value = seed
            for source_category, destination_category in conversion_order:
                value = get_destination_number(
                    conversion_map=conversion_map,
                    source_category=source_category,
                    source_number=value,
                    destination_category=destination_category,
                )
            location_per_seed[seed] = value

        return min(location_per_seed.values())

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        sections = get_sections(lines)
        seed_ranges = get_seeds_by_range(sections.pop(0))
        conversion_order, conversion_map = get_conversion_order_and_maps(sections)
        source_range_per_seed_range = {
            seed_range: seed_range for seed_range in seed_ranges
        }
        for source_category, destination_category in conversion_order:
            next_source_range_per_seed_range = {}
            for seed_range, source_range in source_range_per_seed_range.items():
                destination_range_per_range_seeds = (
                    get_destination_range_per_range_seeds(
                        conversion_map=conversion_map,
                        seed_range=seed_range,
                        source_category=source_category,
                        source_range=source_range,
                        destination_category=destination_category,
                    )
                )

                for (
                    seed_range,
                    destination_range,
                ) in destination_range_per_range_seeds.items():
                    next_source_range_per_seed_range[seed_range] = destination_range
            source_range_per_seed_range = next_source_range_per_seed_range

        return min(
            location_start for location_start, _ in source_range_per_seed_range.values()
        )
