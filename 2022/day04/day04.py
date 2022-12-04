from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/4


def range_overlapping(x, y):
    if x.start == x.stop or y.start == y.stop:
        return False
    return x.start < y.stop and y.start < x.stop


def range_subset(range1, range2):
    """Whether range1 is a subset of range2
    https://stackoverflow.com/a/32481015/463796
    """
    if not range1:
        return True  # empty range is subset of anything
    if not range2:
        return False  # non-empty range can't be subset of empty range
    if len(range1) > 1 and range1.step % range2.step:
        return False  # must have a single value or integer multiple step
    return range1.start in range2 and range1[-1] in range2


def str_to_range(rstr: str):
    l, h = rstr.split("-")
    return range(int(l), int(h) + 1)


def compute_a(file: str) -> int:
    with open(file) as f:
        lines = f.read().splitlines()

    sum = 0
    for line in lines:
        a, b = line.split(",")

        ar = str_to_range(a)
        br = str_to_range(b)
        sum += range_subset(br, ar) or range_subset(ar, br)

    return sum


def compute_b(file):
    with open(file) as f:
        lines = f.read().splitlines()

    sum = 0
    for line in lines:
        a, b = line.split(",")

        ar = str_to_range(a)
        br = str_to_range(b)
        overlap = range_overlapping(ar, br)
        print(f"{ar}, {br}, {overlap}")
        sum += overlap

    return sum


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
    run_expect("test_input.txt", 2, 4)
    run_expect("input.txt", 556, -1)
