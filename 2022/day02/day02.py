from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/2


def compute_a(file):
    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
    # If both players choose the same shape, the round instead ends in a draw.

    # The first column is what your opponent is going to play:
    # A for Rock, B for Paper, and C for Scissors

    # The second column, you reason, must be what you should play in response:
    # X for Rock, Y for Paper, and Z for Scissors.

    df = pd.read_csv(file, header=None, names=["opponent", "you"], delim_whitespace=True)
    df["win"] = df.apply(
        lambda row: (row["opponent"] == "C" and row["you"] == "X")
        or (row["opponent"] == "A" and row["you"] == "Y")
        or (row["opponent"] == "B" and row["you"] == "Z"),
        axis=1,
    )

    df["draw"] = df.apply(
        lambda row: (row["opponent"] == "C" and row["you"] == "Z")
        or (row["opponent"] == "A" and row["you"] == "X")
        or (row["opponent"] == "B" and row["you"] == "Y"),
        axis=1,
    )

    # Your total score is the sum of your scores for each round.

    # The score for a single round is the score for the shape you selected
    # (1 for Rock, 2 for Paper, and 3 for Scissors)

    df["score"] = df.apply(lambda row: 1 if row["you"] == "X" else 2 if row["you"] == "Y" else 3, axis=1)

    # plus the score for the outcome of the round
    # (0 if you lost, 3 if the round was a draw, and 6 if you won)
    df["outcome"] = 0
    df.loc[df["win"], "outcome"] = 6
    df.loc[df["draw"], "outcome"] = 3
    df["total_score"] = df["score"] + df["outcome"]

    return df["total_score"].sum()


def compute_b(file):

    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
    # If both players choose the same shape, the round instead ends in a draw.

    # "Anyway, the second column says how the round needs to end:
    # X means you need to lose, Y means you need to end the round in a draw,
    # and Z means you need to win. Good luck!"

    df = pd.read_csv(file, header=None, names=["opponent", "end"], delim_whitespace=True)
    df["draw"] = False
    df.loc[df["end"] == "Y", "draw"] = True
    df["win"] = False
    df.loc[df["end"] == "Z", "win"] = True
    df["lose"] = False
    df.loc[df["end"] == "X", "lose"] = True

    # The first column is what your opponent is going to play:
    # A for Rock, B for Paper, and C for Scissors

    df["you"] = ""
    df.loc[df["draw"], "you"] = df["opponent"].replace({"A": "X", "B": "Y", "C": "Z"})
    df.loc[df["lose"], "you"] = df["opponent"].replace({"A": "Z", "B": "X", "C": "Y"})
    df.loc[df["win"], "you"] = df["opponent"].replace({"A": "Y", "B": "Z", "C": "X"})

    df["score"] = df.apply(lambda row: 1 if row["you"] == "X" else 2 if row["you"] == "Y" else 3, axis=1)

    # plus the score for the outcome of the round
    # (0 if you lost, 3 if the round was a draw, and 6 if you won)
    df["outcome"] = 0
    df.loc[df["win"], "outcome"] = 6
    df.loc[df["draw"], "outcome"] = 3
    df["total_score"] = df["score"] + df["outcome"]
    return df["total_score"].sum()


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
