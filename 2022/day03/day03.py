from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/3


def priority(common_set):
    assert len(common_set) == 1
    # get only item from set
    item = common_set.pop()
    # Lowercase item types a through z have priorities 1 through 26
    # if item is lowercase:
    if item.islower():
        prior = ord(item) - ord("a") + 1
    else:
        # Uppercase item types A through Z have priorities 27 through 52
        prior = ord(item) - ord("A") + 27

    return prior


def compute_a(file):
    psum = 0
    # read strings per line from file in for loop
    with open(file) as f:
        for line in f:
            line = line.strip()
            # split line in first and second half
            a, b = line[: len(line) // 2], line[len(line) // 2 :]
            assert len(a) == len(b)
            sa = set(a)
            sb = set(b)
            # count common characters
            common = sa & sb

            psum += priority(common)

    return psum


def compute_b(file):

    with open(file) as f:
        lines = f.readlines()

    psum = 0
    # iterate over all lines, three at a time
    for a, b, c in zip(lines[::3], lines[1::3], lines[2::3]):
        # remove trailing newline
        a, b, c = a.strip(), b.strip(), c.strip()

        sa, sb, sc = set(a), set(b), set(c)
        common = sa & sb & sc
        psum += priority(common)

    return psum


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
    run_expect("test_input.txt", 157, 70)
    run_expect("input.txt", 8176, 2689)
