from utils.day import AbstractDay


def get_game_id_and_numbers(line: str) -> tuple[int, list[int], list[int]]:
    game, unsplit_numbers = line.split(": ")
    game_id = int(game[len("Card ") :])
    raw_winning_numbers, raw_numbers = unsplit_numbers.split("| ")
    return (
        game_id,
        [int(num) for num in raw_winning_numbers.split(" ") if num != ""],
        [int(num) for num in raw_numbers.split(" ") if num != ""],
    )


def count_matching_numbers(winning_numbers: list[int], numbers: list[int]) -> int:
    winning_numbers_set = set(winning_numbers)
    return sum((num in winning_numbers_set) for num in numbers)


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        total_points = 0
        for line in lines:
            game_id, winning_numbers, numbers = get_game_id_and_numbers(line)
            if count_match := count_matching_numbers(winning_numbers, numbers):
                total_points += 2 ** (count_match - 1)
        return total_points

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        matching_count_per_game_id = {}
        for line in lines:
            game_id, winning_numbers, numbers = get_game_id_and_numbers(line)
            matching_count_per_game_id[game_id] = count_matching_numbers(
                winning_numbers, numbers
            )
        game_ids = list(matching_count_per_game_id.keys())
        total_copies_per_game_id = {game_id: 1 for game_id in game_ids}
        for game_id, matching_count in matching_count_per_game_id.items():
            for _ in range(total_copies_per_game_id[game_id]):
                for i in range(
                    game_id + 1,
                    min(game_id + 1 + matching_count, game_ids[-1] + 1),
                ):
                    total_copies_per_game_id[i] += 1
        return sum(total_copies for _, total_copies in total_copies_per_game_id.items())
