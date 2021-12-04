import numpy as np
import pandas as pd
from funcy import print_durations


def read_bingo(file):

    with open(file, "r") as f:
        drawn = f.readline()

    drawn = [int(num) for num in drawn.strip().split(",")]

    boards = pd.read_csv(file, header=None, skiprows=1)
    boards = boards[0].apply(str.split)

    boards = pd.DataFrame(boards.tolist()).astype(int)
    boards = boards.values.reshape((-1, 5, 5))
    return drawn, boards


@print_durations
def day4a(file):

    drawn, boards = read_bingo(file)

    matches = np.zeros_like(boards, dtype=bool)

    for draw in drawn:
        matches[boards == draw] = True

        has_match_a1 = matches.all(axis=1).any(axis=1)
        has_match_a2 = matches.all(axis=2).any(axis=1)

        has_match = has_match_a1 + has_match_a2

        if has_match.any():
            winning_board_id = has_match.argmax()
            winning_board = boards[winning_board_id]
            winning_matches = matches[winning_board_id]
            return winning_board[~winning_matches].sum() * draw


@print_durations
def day4b(file):

    drawn, boards = read_bingo(file)

    matches = np.zeros_like(boards, dtype=bool)

    has_won = np.zeros(boards.shape[0], dtype=bool)

    for draw in drawn:
        matches[boards == draw] = True

        has_match_a1 = matches.all(axis=1).any(axis=1)
        has_match_a2 = matches.all(axis=2).any(axis=1)

        has_match = has_match_a1 + has_match_a2

        if has_match.sum() == boards.shape[0] and has_won.sum() < boards.shape[0]:
            winning_board_id = has_won.argmin()
            winning_board = boards[winning_board_id]
            winning_matches = matches[winning_board_id]
            return winning_board[~winning_matches].sum() * draw

        has_won += has_match


if __name__ == "__main__":

    print(f"Day 4a: {day4a('input.txt')}")
    print(f"Day 4b: {day4b('input.txt')}")

    assert day4a("test_input.txt") == 4512
    assert day4b("test_input.txt") == 1924

    assert day4a("input.txt") == 89001
    assert day4b("input.txt") == 7296
