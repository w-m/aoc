from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd
from copy import copy
from collections import deque

# https://adventofcode.com/2022/day/6


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    # The device will send your subroutine a datastream buffer (your puzzle input)

    # In the protocol being used by the Elves, the start of a packet is indicated
    # by a sequence of four characters that are all different.

    # Specifically, it needs to report the number of characters from the beginning
    # of the buffer to the end of the first such four-character marker.

    # For example, suppose you receive the following datastream buffer:
    # mjqjpqmgbljsphdztnvjfqwrcgsmlb
    # The first time a marker appears is after the seventh character arrives.

    with open(file) as f:
        line = f.read().strip()

    deq = deque([], maxlen=4)
    for i, char in enumerate(line):
        deq.append(char)
        if len(set(deq)) == 4:
            # yield i - 3
            yield i + 1
            break

    deq = deque([], maxlen=14)
    for i, char in enumerate(line):
        deq.append(char)
        if len(set(deq)) == 14:
            # yield i - 3
            yield i + 1
            break


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
    run_expect("test_input.txt", 7, 19)
    run_expect("input.txt", 1275, 3605)
