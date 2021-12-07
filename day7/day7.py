from funcy import print_durations
from collections import Counter, defaultdict
import numpy as np
from tqdm import trange


@print_durations
def day7(file):

    hpos = np.loadtxt(file, delimiter=",", dtype=int)

    # median is the point with same distance to each half
    best_pos = np.median(hpos).astype(int)
    diffs = hpos - best_pos
    yield np.abs(diffs).sum()

    min_steps = 1e8

    # how to find the exact best point?
    # coincidentally its the rounded down mean for my data
    # -> 489, with mean 489.591. how come?
    # bp2 = np.round(np.mean(hpos)).astype(int)

    for bp2 in trange(np.max(hpos)):

        d2 = np.abs(hpos - bp2)

        # Gauss formula
        steps = ((d2 * (d2 + 1)) // 2).sum()

        if steps < min_steps:
            min_steps = steps

    yield min_steps


if __name__ == "__main__":
    test_a, test_b = day7("test_input.txt")
    puzzle_a, puzzle_b = day7("input.txt")

    print(f"Day 7a: {test_a}")
    print(f"Day 7b: {test_b}")

    print(f"Day 7a: {puzzle_a}")
    print(f"Day 7b: {puzzle_b}")

    assert test_a == 37
    assert test_b == 168

    assert puzzle_a == 356179
    assert puzzle_b == 99788435
