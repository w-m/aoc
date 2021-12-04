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


def eval_bingo(draws, boards):

    matches = np.zeros_like(boards, dtype=bool)
    has_won = np.zeros(boards.shape[0], dtype=bool)

    for draw in draws:
        matches[boards == draw] = True

        has_match_a1 = matches.all(axis=1).any(axis=1)
        has_match_a2 = matches.all(axis=2).any(axis=1)

        has_match = has_match_a1 | has_match_a2

        new_winner = has_match & ~has_won

        if new_winner.any():
            winning_board_id = new_winner.argmax()
            winning_board = boards[winning_board_id]
            winning_matches = matches[winning_board_id]
            yield winning_board[~winning_matches].sum() * draw

        has_won = has_match


@print_durations
def day4(file):
    draws, boards = read_bingo(file)
    bingo_winner_generator = eval_bingo(draws, boards)
    first = next(bingo_winner_generator)
    for last in bingo_winner_generator:
        pass
    return first, last


if __name__ == "__main__":

    day4a_test, day4b_test = day4("test_input.txt")
    day4a_puzzle, day4b_puzzle = day4("input.txt")

    print(f"Day 4a: {day4a_puzzle}")
    print(f"Day 4b: {day4b_puzzle}")

    assert day4a_test == 4512
    assert day4b_test == 1924

    assert day4a_puzzle == 89001
    assert day4b_puzzle == 7296
