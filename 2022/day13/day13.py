import os.path
from typing import Iterator, List, Optional

from funcy import print_durations
from functools import cmp_to_key

# https://adventofcode.com/2022/day/13


def compare(a, b):

    if isinstance(a, int) and isinstance(b, int):
        # the lower integer should come first
        return a - b

    if isinstance(a, list) and isinstance(b, list):
        # zip
        for a_, b_ in zip(a, b):
            res = compare(a_, b_)
            # If the lists are the same length and no comparison makes a decision
            # about the order, continue checking the next part of the input
            if res != 0:
                return res

        # If the left list runs out of items first, the inputs are in the right order
        return compare(len(a), len(b))

    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])

    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file, "r") as f:
        pairs = f.read().split("\n\n")

    packets = []

    # what is the sum of the indices of the packets that are in order?
    osum = 0
    for idx, pair_str in enumerate(pairs, start=1):
        a, b = pair_str.split("\n")
        a, b = eval(a), eval(b)
        if compare(a, b) < 0:
            osum += idx
        packets.extend((a, b))

    yield osum

    # special packets for part 2
    s0, s1 = [[2]], [[6]]
    packets.extend((s0, s1))

    # Organize all of the packets into the correct order
    ps = sorted(packets, key=cmp_to_key(compare))

    # determine the indices of the two divider packets
    # and multiply them together
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
