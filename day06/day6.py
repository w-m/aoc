from funcy import print_durations
from collections import Counter, defaultdict
import numpy as np


@print_durations
def day6(file, num_simulation_days):

    # you can model each fish as a single number that represents
    # the number of days until it creates a new lanternfish
    fish_days = np.loadtxt(file, delimiter=",", dtype=int)

    # count fish by their countdown day
    fish_day_counter = dict(Counter(fish_days))

    for day in range(num_simulation_days):

        updated_counter = defaultdict(int)

        for day_countdown, numfish in fish_day_counter.items():
            if day_countdown == 0:
                # a lanternfish that creates a new fish resets its timer to 6
                updated_counter[6] += numfish
                # the new lanternfish starts with an internal timer of 8
                updated_counter[8] += numfish
            else:
                updated_counter[day_countdown - 1] += numfish

        fish_day_counter = updated_counter

    return sum(fish_day_counter.values())


if __name__ == "__main__":
    test_a, test_b = day6("test_input.txt", 80), day6("test_input.txt", 256)
    puzzle_a, puzzle_b = day6("input.txt", 80), day6("input.txt", 256)

    print(f"Day 6a: {test_a}")
    print(f"Day 6b: {test_b}")

    print(f"Day 6a: {puzzle_a}")
    print(f"Day 6b: {puzzle_b}")

    assert test_a == 5934
    assert test_b == 26984457539

    assert puzzle_a == 365862
    assert puzzle_b == 1653250886439
