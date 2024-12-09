from utils.day import AbstractDay


class Day(AbstractDay):

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        disk_map = list(map(int, list(lines[0])))
        disk = []
        id_number = 0
        free_spaces = []
        while disk_map:
            disk.extend([id_number] * disk_map.pop(0))
            id_number += 1
            if disk_map:
                free_space_length = disk_map.pop(0)
                index_begin = len(disk)
                disk.extend(["."] * free_space_length)
                free_spaces.extend(range(index_begin, index_begin + free_space_length))

        # we switch each ending non-free disk with a free space
        # for the last N places (with N the number of free spaces)
        for i in range(1, len(free_spaces) + 1):
            if disk[-i] != ".":
                j = free_spaces.pop(0)
                disk[-i], disk[j] = ".", disk[-i]

        return sum(
            i * id_number for i, id_number in enumerate(disk) if id_number != "."
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        disk_map = list(map(int, list(lines[0])))
        disk = []
        id_number = 0
        free_spaces: list[tuple[int, int]] = []  # (index_begin, length)
        number_data: dict[int, tuple[int, int]] = (
            {}
        )  # index_begin and length per id_number
        while disk_map:
            id_number_length = disk_map.pop(0)
            index_begin = len(disk)
            disk.extend([id_number] * id_number_length)
            number_data[id_number] = (index_begin, id_number_length)
            id_number += 1
            if disk_map:
                free_space_length = disk_map.pop(0)
                index_begin = len(disk)
                disk.extend(["."] * free_space_length)
                free_spaces.append((index_begin, free_space_length))

        for id_number in sorted(number_data, reverse=True):
            index_begin, length = number_data[id_number]
            for j in range(len(free_spaces)):
                free_space_index_begin, free_space_length = free_spaces[j]
                if free_space_index_begin > index_begin:
                    # the free space is after the id_numbers
                    break
                if free_space_length >= length:
                    for k in range(length):

                        disk[index_begin + k] = "."
                        disk[free_space_index_begin + k] = id_number

                    if free_space_length == length:
                        free_spaces.pop(j)
                    else:
                        free_spaces[j] = (
                            free_space_index_begin + length,
                            free_space_length - length,
                        )
                    break

        return sum(
            i * id_number for i, id_number in enumerate(disk) if id_number != "."
        )
