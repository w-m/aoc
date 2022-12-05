from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/4


def range_overlapping(range_a, range_b):
    """Are the values in the two ranges overlapping at all?"""
    return range_a.start < range_b.stop and range_b.start < range_a.stop


def range_subset(range_a, range_b):
    """Whether range1 is a subset of range2"""
    return range_a.start in range_b and range_a[-1] in range_b


def str_to_range(range_str: str):
    """range_str like "1-3" (elf range: inclusive) -> range(1, 4) Python"""
    l, h = range_str.split("-")
    return range(int(l), int(h) + 1)


def compute_query(file: str, query) -> int:
    with open(file) as f:
        ranges = (map(str_to_range, line.strip().split(",")) for line in f)
        return sum(query(range_a, range_b) for range_a, range_b in ranges)


def compute_a(file: str) -> int:
    is_either_subset = lambda ar, br: range_subset(ar, br) or range_subset(br, ar)
    return compute_query(file, is_either_subset)


def compute_b(file):
    return compute_query(file, range_overlapping)


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
    run_expect("input.txt", 556, 876)
