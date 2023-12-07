from dataclasses import dataclass
from enum import Enum

from utils.day import AbstractDay


@dataclass
class Card:
    label: str
    value: int


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, raw_hand: str, bid: int):
        self.cards: tuple[Card, Card, Card, Card, Card] = tuple(
            CARD_BY_LABEL[label] for label in raw_hand
        )
        self.bid = bid
        self.handtype = self._get_handtype()

    def _get_handtype(self) -> HandType:
        count_per_label = self._count_per_label()
        counts = sorted(count_per_label.values())
        if self.has_n_of_a_kind(5, counts):
            return HandType.FIVE_OF_A_KIND
        if self.has_n_of_a_kind(4, counts):
            return HandType.FOUR_OF_A_KIND
        if self.has_full_house(counts):
            return HandType.FULL_HOUSE
        if self.has_n_of_a_kind(3, counts):
            return HandType.THREE_OF_A_KIND
        if self.has_two_pairs(counts):
            return HandType.TWO_PAIRS
        if self.has_n_of_a_kind(2, counts):
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def _count_per_label(self) -> dict[str, int]:
        count_per_label = {}
        for card in self.cards:
            count_per_label[card.label] = count_per_label.get(card.label, 0) + 1
        return count_per_label

    def has_n_of_a_kind(self, n: int, counts: dict[str, int]) -> bool:
        return n in counts

    def has_full_house(self, counts: dict[str, int]) -> bool:
        return counts == [2, 3]

    def has_two_pairs(self, counts) -> bool:
        return counts == [1, 2, 2]

    def __lt__(self, other: "Hand") -> bool:
        if self.handtype == other.handtype:
            for card1, card2 in zip(self.cards, other.cards):
                if card1.value == card2.value:
                    continue
                return card1.value < card2.value
            assert False, "There are two same hands"
        return self.handtype.value < other.handtype.value


CARD_BY_LABEL = {str(i): Card(str(i), i) for i in range(2, 10)} | {
    label: Card(label, value) for value, label in enumerate("TJQKA", 10)
}


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        hands: list[Hand] = []
        for line in lines:
            raw_hand, bid = line.split(" ")
            hands.append(Hand(raw_hand, int(bid)))
        hands.sort()
        return sum([rank * hand.bid for rank, hand in enumerate(hands, 1)])

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        return None
