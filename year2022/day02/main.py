from enum import Enum

from utils.day import AbstractDay


class Shapes(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class Players(Enum):
    PLAYER1 = 1
    PLAYER2 = 2


cast_from_player = {
    Players.PLAYER1: {"A": Shapes.ROCK, "B": Shapes.PAPER, "C": Shapes.SCISSORS},
    Players.PLAYER2: {"X": Shapes.ROCK, "Y": Shapes.PAPER, "Z": Shapes.SCISSORS},
}
SCORE_SHAPE = {Shapes.ROCK: 1, Shapes.PAPER: 2, Shapes.SCISSORS: 3}
SCORE_WIN, SCORE_DRAW, SCORE_DEFEAT = 6, 3, 0

shapes_list = [Shapes.ROCK, Shapes.PAPER, Shapes.SCISSORS]
# given the shape of index i:
# -> shape i+1 beats it
# -> shape i-1 loses against it


def get_shape_for_lose(shape: Shapes) -> Shapes:
    return shapes_list[(shapes_list.index(shape) - 1) % len(shapes_list)]


def get_shape_for_win(shape: Shapes) -> Shapes:
    return shapes_list[(shapes_list.index(shape) + 1) % len(shapes_list)]


def get_shape_for_draw(shape: Shapes) -> Shapes:
    return shape


def get_winner(
    shape1: Shapes,
    shape2: Shapes,
) -> Players | None:
    """
    Return the winning player or None if draw
    """
    if shape1 == shape2:
        return None
    if (shape1, shape2) in {
        (Shapes.ROCK, Shapes.SCISSORS),
        (Shapes.SCISSORS, Shapes.PAPER),
        (Shapes.PAPER, Shapes.ROCK),
    }:
        return Players.PLAYER1
    return Players.PLAYER2


def get_score_for_player2(
    shape1: Shapes,
    shape2: Shapes,
):
    """
    Given the shape of player 1 and player 2
    Returns the score of player 2
     ie (score of the Player2' shape) + (score of winning/drawing/losing)
    """
    score = SCORE_SHAPE[shape2]
    winner = get_winner(shape1=shape1, shape2=shape2)
    if winner is Players.PLAYER1:
        return score + SCORE_DEFEAT
    if winner is None:
        return score + SCORE_DRAW
    return score + SCORE_WIN


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        total_score = 0
        for line in lines:
            original_shape1, original_shape2 = line.split(" ")
            total_score += get_score_for_player2(
                shape1=cast_from_player[Players.PLAYER1][original_shape1],
                shape2=cast_from_player[Players.PLAYER2][original_shape2],
            )
        return total_score

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        total_score = 0
        fun_and_score_by_strategy = {
            "X": (get_shape_for_lose, SCORE_DEFEAT),
            "Y": (get_shape_for_draw, SCORE_DRAW),
            "Z": (get_shape_for_win, SCORE_WIN),
        }
        for line in lines:
            original_shape1, strategy = line.split(" ")
            shape1 = cast_from_player[Players.PLAYER1][original_shape1]
            get_shape2_from_shape1, score = fun_and_score_by_strategy[strategy]
            shape2 = get_shape2_from_shape1(shape1)
            total_score += score + SCORE_SHAPE[shape2]
        return total_score
