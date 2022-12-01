from funcy import print_durations
import numpy as np
import pandas as pd
import os.path
from collections import deque, Counter, defaultdict


def compute(file):
    with open(file, "r") as f:
        split_elves = f.read().split("\n\n")
        elf_calories = [elf.split("\n") for elf in split_elves]

    caloric_sums = []
    for elf in elf_calories:
        caloric_sum = 0
        for calories in elf:
            caloric_sum += int(calories)
        caloric_sums.append(caloric_sum)

    yield max(caloric_sums)

    yield sum(sorted(caloric_sums, reverse=True)[:3])


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
    run_expect("test_input.txt", 24000, 45000)
    run_expect("input.txt", 67016, 200116)
