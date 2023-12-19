from typing import TypeAlias

Range: TypeAlias = tuple[int, int]


def get_intersection(r1: Range, r2: Range) -> Range | None:
    """Return the intersection of [a1, b1] and [a2, b2]"""
    left, right = (max(r1[0], r2[0]), min(r1[1], r2[1]))
    return None if left > right else (left, right)


def get_global_union(r1: Range, r2: Range) -> Range:
    """
    Return the union of [a1, b1] and [a2, b2]
    without holes
    """
    return (min(r1[0], r2[0]), max(r1[1], r2[1]))


def get_exclusive_union(r1: Range, r2: Range) -> tuple[Range | None, Range | None]:
    """
    Return the left and right exclusion of [a1, b1] and [a2, b2]
     ie ranges outside the intersection (but inside the union)
    """
    intersection = get_intersection(r1, r2)
    if intersection is None:
        return (r1, r2) if r1[0] < r2[0] else (r2, r1)
    union = get_global_union(r1, r2)
    left_exclusion = (
        None if union[0] == intersection[0] else (union[0], intersection[0])
    )
    right_exclusion = (
        None if union[1] == intersection[1] else (intersection[1], union[1])
    )
    return left_exclusion, right_exclusion


def merge(ranges: list[Range]) -> list[Range]:
    """
    Merge overlapping ranges
    """
    ranges = sorted(ranges, key=lambda r: r[0])
    new_ranges = []
    while ranges:
        new_ranges.append(ranges.pop(0))
        while ranges and new_ranges[-1][1] >= ranges[0][0]:
            new_ranges[-1] = (new_ranges[-1][0], max(new_ranges[-1][1], ranges[0][1]))
            ranges.pop(0)
    return new_ranges


def _cut_ranges(ranges: list[Range], cutting_ranges: list[Range]) -> list[Range]:
    new_ranges = []
    while cutting_ranges:
        while cutting_ranges[0][1] < ranges[0][0]:
            # cut range is strictly outside the ranges
            cutting_ranges.pop(0)
            if not cutting_ranges:
                new_ranges.extend(ranges)
                return new_ranges
        # ranges[0][0] <= cutting_ranges[0][1]
        while ranges and cutting_ranges and ranges[0][0] <= cutting_ranges[0][1]:
            if ranges[0][1] < cutting_ranges[0][0]:
                # the first range does not overlap with the first cutting range
                new_ranges.append(ranges.pop(0))
            else:
                # the first range and the first cutting range has an intersection
                if ranges[0][1] >= cutting_ranges[0][1]:
                    # the cutting range ends before the end of the range
                    if ranges[0][0] < cutting_ranges[0][0]:
                        # the first range fully contains the first cutting range
                        new_ranges.append((ranges[0][0], cutting_ranges[0][0] - 1))
                        new_ranges.append((cutting_ranges[0][0], cutting_ranges[0][1]))
                        if ranges[0][1] > cutting_ranges[0][1]:
                            ranges[0] = (cutting_ranges[0][1] + 1, ranges[0][1])
                    else:
                        # first cutting range begins with the first range
                        new_ranges.append((ranges[0][0], cutting_ranges[0][1]))
                        if ranges[0][1] > cutting_ranges[0][1]:
                            # if cutting ranges strictly ends up before end of range
                            #  then we insert the rest of the range as first range
                            ranges[0] = (
                                max(cutting_ranges[0][1] + 1, ranges[0][0]),
                                ranges[0][1],
                            )
                        else:
                            # otherwise we remove the first range
                            #  as ranges[0][1] == cutting_ranges[0][1]
                            ranges.pop(0)
                    cutting_ranges.pop(0)
                    if not cutting_ranges:
                        new_ranges.extend(ranges)
                        return new_ranges
                else:
                    # the cutting range ends after the end of the range
                    if ranges[0][0] >= cutting_ranges[0][0]:
                        # the cutting range fully contains the first range
                        new_ranges.append((ranges[0][0], ranges[0][1]))
                    else:
                        new_ranges.append((ranges[0][0], cutting_ranges[0][0] - 1))
                        new_ranges.append((cutting_ranges[0][0], ranges[0][1]))
                    ranges.pop(0)
        if not ranges:
            return new_ranges
    return new_ranges


def get_distinct_by(ranges: list[Range], cutting_ranges: list[Range]) -> list[Range]:
    """
    Split ranges of first argument so that
     they cannot strictly contains any of the ranges of the second argument

    This assumes that for each argument, the ranges are not overlapping
    """
    if not cutting_ranges:
        return ranges

    # sort ranges by starting point
    ranges = sorted(ranges, key=lambda r: r[0])
    cutting_ranges = sorted(cutting_ranges, key=lambda r: r[0])

    new_ranges = _cut_ranges(ranges, cutting_ranges)
    return new_ranges
