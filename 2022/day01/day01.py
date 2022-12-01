from funcy import print_durations
import numpy as np
import pandas as pd
import os.path
from collections import deque, Counter, defaultdict


def compute(file):
    with open(file, "r") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    cur_elf = 0
    max_cal = 0
    for line in lines:
        if len(line):
            cur_elf += int(line)
        else:
            max_cal = max(max_cal, cur_elf)
            cur_elf = 0

    yield max_cal

    elves = []
    cur_elf = 0
    for line in lines:
        if len(line):
            cur_elf += int(line)
        else:
            elves.append(cur_elf)
            cur_elf = 0

    if cur_elf > 0:
        elves.append(cur_elf)

    elves = sorted(elves)

    yield sum(elves[-3:])


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
