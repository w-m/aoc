from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/2


def compute_score(df):
    # The score for a single round is the score for the shape you selected
    # (1 for Rock, 2 for Paper, and 3 for Scissors)
    df["score"] = df["you"] + 1

    # plus the score for the outcome of the round
    # (0 if you lost, 3 if the round was a draw, and 6 if you won)
    df["outcome"] = df["win"] * 6 + df["draw"] * 3

    df["total_score"] = df["score"] + df["outcome"]

    # Your total score is the sum of your scores for each round.
    return df["total_score"].sum()


def compute_a(file):
    df = pd.read_csv(file, header=None, names=["opponent", "you"], delim_whitespace=True)

    # The first column is what your opponent is going to play:
    # A for Rock, B for Paper, and C for Scissors
    df["opponent"] = df["opponent"].replace({"A": 0, "B": 1, "C": 2})

    # The second column, you reason, must be what you should play in response:
    # X for Rock, Y for Paper, and Z for Scissors.
    df["you"] = df["you"].replace({"X": 0, "Y": 1, "Z": 2})

    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
    df["win"] = df["you"] == (df["opponent"] + 1) % 3

    # If both players choose the same shape, the round instead ends in a draw.
    df["draw"] = df["you"] == df["opponent"]

    return compute_score(df)


def compute_b(file):
    df = pd.read_csv(file, header=None, names=["opponent", "end"], delim_whitespace=True)

    # The first column is what your opponent is going to play:
    # A for Rock, B for Paper, and C for Scissors
    df["opponent"] = df["opponent"].replace({"A": 0, "B": 1, "C": 2})

    # "Anyway, the second column says how the round needs to end:
    # X means you need to lose, Y means you need to end the round in a draw,
    # and Z means you need to win. Good luck!"
    df["lose"] = df["end"] == "X"
    df["draw"] = df["end"] == "Y"
    df["win"] = df["end"] == "Z"

    # default: lose
    df["you"] = (df.opponent + 2) % 3
    df.loc[df.draw, "you"] = df.loc[df.draw, "opponent"]
    df.loc[df.win, "you"] = (df.loc[df.win, "opponent"] + 1) % 3

    return compute_score(df)


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    yield compute_a(file)
    yield compute_b(file)


@print_durations
def run_expect(file, result_a, result_b):
    a, b = compute(file)
    prefix = os.path.basename(__file__)
    print(f"{prefix} {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"{prefix} {file}: {b}")
        assert b == result_b


if __name__ == "__main__":
    run_expect("test_input.txt", 15, 12)
    run_expect("input.txt", 12586, 13193)
