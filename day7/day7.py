from funcy import print_durations
from collections import Counter, defaultdict
import numpy as np
from tqdm import trange


@print_durations
def day7(file):

    hpos = np.loadtxt(file, delimiter=",", dtype=int)

    best_pos = np.median(hpos).astype(int)
    diffs = hpos - best_pos

    min_steps = 1e8

    for bp2 in trange(np.max(hpos)):

        #        bp2 = np.round(np.mean(hpos)).astype(int)
        d2 = np.abs(hpos - bp2)

        steps = 0
        cur_step = 1

        while d2.any():
            mask = d2 > 0
            d2[mask] -= 1
            steps += cur_step * mask.sum()
            cur_step += 1

        if steps < min_steps:
            min_steps = steps

    return np.abs(diffs).sum(), min_steps


if __name__ == "__main__":
    test_a, test_b = day7("test_input.txt")
    puzzle_a, puzzle_b = day7("input.txt")

    print(f"Day 7a: {test_a}")
    print(f"Day 7b: {test_b}")

    print(f"Day 7a: {puzzle_a}")
    print(f"Day 7b: {puzzle_b}")

    assert test_a == 37
    assert test_b == 26984457539

    assert puzzle_a == 356179
    assert puzzle_b == 1653250886439
