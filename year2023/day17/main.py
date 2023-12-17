from heapq import heapify, heappop, heappush

from utils.day import AbstractDay
from utils.grid2D import Directions, Grid, Position, scalar_product


def dijkstra(grid: Grid, min_forward: int = 1, max_forward: int = 3) -> int:
    pqueue = [(0, 0, 0, 0, 0)]  # distance_from_start, *position, *direction
    visited = set()
    heapify(pqueue)
    while pqueue:
        distance_from_start, x, y, dx, dy = heappop(pqueue)
        if (x, y) == (len(grid.lines[0]) - 1, len(grid.lines) - 1):
            return distance_from_start
        if (x, y, dx, dy) in visited:
            continue
        visited.add((x, y, dx, dy))
        for direction in Directions:
            if scalar_product(*direction.value, dx, dy) != 0:
                continue
            new_position = Position(x, y)
            new_distance = distance_from_start
            for i in range(1, max_forward + 1):
                new_position = new_position.move(direction)
                if value := grid.get_from_position(new_position):
                    new_distance += int(value)
                    if i >= min_forward:
                        heappush(
                            pqueue,
                            (
                                new_distance,
                                new_position.x,
                                new_position.y,
                                *direction.value,
                            ),
                        )


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return dijkstra(Grid(lines))

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return dijkstra(Grid(lines), min_forward=4, max_forward=10)
