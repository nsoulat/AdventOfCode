from pathlib import Path

from utils.file import read_file_line_by_line

from ..main import Day, Hand, HandType

tests_dir = Path(__file__).parent


def test_part1():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part1 = Day.resolve_part1(input_)
    assert result_part1 == 6440, "Part 1 is incorrect"


def test_part2():
    input_ = read_file_line_by_line(tests_dir / "test01.txt")
    result_part2 = Day.resolve_part2(input_)
    assert result_part2 == 5905, "Part 2 is incorrect"


raw_hands_for_tests = [
    # raw hands, expected handtype, expected rank
    ("26J35", HandType.ONE_PAIR, 1),
    ("T55J5", HandType.FOUR_OF_A_KIND, 5),
    ("J888J", HandType.FIVE_OF_A_KIND, 6),
    ("KAKAK", HandType.FULL_HOUSE, 3),
    ("2AAAA", HandType.FOUR_OF_A_KIND, 4),
    ("33333", HandType.FIVE_OF_A_KIND, 7),
    ("J4452", HandType.THREE_OF_A_KIND, 2),
]


def test_compare_hands():
    hands: list[Hand] = []
    for raw_hand, expected_handtype, _ in raw_hands_for_tests:
        hand = Hand(raw_hand=raw_hand, bid=1, activate_joker=True)
        assert hand.handtype is expected_handtype, str(hand)
        hands.append(hand)

    hands.sort()
    assert all(
        str(hands[rank - 1]) == raw_hand for raw_hand, _, rank in raw_hands_for_tests
    )
