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
    def __init__(self, raw_hand: str, bid: int, activate_joker: bool = False):
        self.joker_activated = activate_joker
        self.cards: tuple[Card, Card, Card, Card, Card] = tuple(
            CARD_BY_LABEL[label] for label in raw_hand
        )
        if self.joker_activated:
            self.joker_count = 0
            for card in self.cards:
                if card.label == "J":
                    card.value = 1
                    self.joker_count += 1

        self.bid = bid
        self.handtype = self._get_handtype()

    def _get_handtype(self) -> HandType:
        count_per_label = self._count_per_label()
        if self.joker_activated and self.joker_count:
            del count_per_label["J"]
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
        return n in counts or (
            self.joker_activated
            and ((max(counts) if counts else 0) + self.joker_count >= n)
        )

    def has_full_house(self, counts: dict[str, int]) -> bool:
        return counts == [2, 3] or (
            self.joker_activated and self.joker_count and len(counts) == 2
        )

    def has_two_pairs(self, counts) -> bool:
        return counts == [1, 2, 2] or (
            self.joker_activated
            and ((self.joker_count == 1 and len(counts) <= 3) or (self.joker_count > 1))
        )

    def __lt__(self, other: "Hand") -> bool:
        if self.handtype == other.handtype:
            for card1, card2 in zip(self.cards, other.cards):
                if card1.value == card2.value:
                    continue
                return card1.value < card2.value
            assert False, "There are two same hands"
        return self.handtype.value < other.handtype.value

    def __str__(self) -> str:
        return "".join(card.label for card in self.cards)


CARD_BY_LABEL = {str(i): Card(str(i), i) for i in range(2, 10)} | {
    label: Card(label, value) for value, label in enumerate("TJQKA", 10)
}


class Day(AbstractDay):
    @classmethod
    def _resolve(cls, lines: list[str], activate_joker: bool):
        hands: list[Hand] = []
        for line in lines:
            raw_hand, bid = line.split(" ")
            hands.append(Hand(raw_hand, int(bid), activate_joker))
        hands.sort()
        return sum([rank * hand.bid for rank, hand in enumerate(hands, 1)])

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return cls._resolve(lines, activate_joker=False)

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        return cls._resolve(lines, activate_joker=True)
