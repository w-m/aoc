from funcy import print_durations
import itertools
import numpy as np
from collections import defaultdict, Counter
import functools


# Puzzle: https://adventofcode.com/2021/day/21

# game board with spaces 1 to 10, two players
# after 10, wraps around to 1
# 100-sided die, rolls 1,2,3,...100,1,2,3...
# each player's turn, the player rolls the die three times
# and adds up the results. Then, the player moves their pawn that many times forward
# score: add current field
# 1000 points wins


def create_die(maxnum):
    yield from enumerate(itertools.cycle(range(1, maxnum + 1)), 1)


def wrap_around(field):
    if field > 10:
        field %= 10
    if field == 0:
        field = 10
    return field


def player(startfield, die):
    score = 0
    field = startfield
    while True:
        walk = 0
        for i in range(3):
            diecount, dieval = next(die)
            walk += dieval

        field += walk
        field = wrap_around(field)
        score += field
        yield diecount, score


def step_count_dict():
    x = []
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                x.append((i, j, k))

    step_counts = np.unique(np.array(x).sum(axis=1), return_counts=True)

    # {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    return {step: count for step, count in zip(step_counts[0], step_counts[1])}


scd = step_count_dict()


@print_durations
def day21a(p1_start, p2_start):

    die = create_die(100)

    p1 = player(p1_start, die)
    p2 = player(p2_start, die)

    while True:
        diecount, s1 = next(p1)

        if s1 >= 1000:
            return s2 * diecount

        diecount, s2 = next(p2)

        if s2 >= 1000:
            return s1 * diecount

    # what do you get if you multiply the score of the losing player
    # by the number of times the die was rolled during the game


@functools.cache
def count_num_wins(p1_field, p1_score, p2_field, p2_score):

    # p1 is throwing dice

    # when calling day21b for next move, switch p1 and p2 in arguments
    # When adding up -> switch back

    p1_sum = 0
    p2_sum = 0

    for field_movement, num_throws in scd.items():
        p1_field_new = p1_field + field_movement
        p1_field_new = wrap_around(p1_field_new)
        p1_score_new = p1_score + p1_field_new

        if p1_score_new >= 21:
            # p1 wins 1, p2 wins 0
            p1_sum += num_throws
        else:
            # go again
            p2_win, p1_win = count_num_wins(p2_field, p2_score, p1_field_new, p1_score_new)
            p1_sum += p1_win * num_throws
            p2_sum += p2_win * num_throws

    return p1_sum, p2_sum


@print_durations
def day21b(p1_start, p2_start):
    return max(count_num_wins(p1_start, 0, p2_start, 0))


if __name__ == "__main__":
    print(day21a(4, 8))
    assert day21a(4, 8) == 739785
    print(day21a(8, 9))
    assert count_num_wins(4, 0, 8, 0) == (444356092776315, 341960390180808)
    assert day21b(8, 9) == 346642902541848
