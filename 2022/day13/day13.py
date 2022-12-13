import os.path
from collections import *
from copy import copy
from typing import Iterator, List, Optional

import numpy as np
import pandas as pd
from funcy import print_durations
from functools import cmp_to_key

# https://adventofcode.com/2022/day/xx


def compare(a, b):
    # return True if in right order
    # both values are int? a should be lower
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        if a == b:
            return 0
        if a > b:
            return 1
    # both are lists? compare each element
    if isinstance(a, list) and isinstance(b, list):
        # zip
        for a_, b_ in zip(a, b):
            res = compare(a_, b_)
            if res != 0:
                return res

        return compare(len(a), len(b))
    # a is list, b is int? make b a singleton list
    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    # a is int, b is list? make a a singleton list
    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file, "r") as f:
        pairs = f.read().split("\n\n")

    packets = []

    osum = 0
    for idx, pair_str in enumerate(pairs, start=1):
        p0, p1 = pair_str.split("\n")
        p0 = eval(p0)
        p1 = eval(p1)
        res = compare(p0, p1)
        print(f"{idx}: {res} \t {p0} - {p1}")
        if res == -1:
            osum += idx
        packets.append(p0)
        packets.append(p1)

    yield osum

    s0 = [[2]]
    s1 = [[6]]

    packets.append(s0)
    packets.append(s1)

    ps = sorted(packets, key=cmp_to_key(compare))
    yield (ps.index(s0) + 1) * (ps.index(s1) + 1)


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
    run_expect("test_input.txt", 13, 140)
    run_expect("input.txt", 6187, 23520)
