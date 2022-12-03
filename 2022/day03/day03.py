from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd

# https://adventofcode.com/2022/day/3


def priority(common_chars: set) -> int:
    assert len(common_chars) == 1
    item = common_chars.pop()

    # Lowercase item types a through z have priorities 1 through 26
    if item.islower():
        prior = ord(item) - ord("a") + 1
    # Uppercase item types A through Z have priorities 27 through 52
    else:
        prior = ord(item) - ord("A") + 27

    return prior


def common_compartment_priority(line: str) -> int:
    # The list of items for each rucksack is given as characters all on a single line.
    # A given rucksack always has the same number of items in each of its two compartments,
    # so the first half of the characters represent items in the first compartment,
    # while the second half of the characters represent items in the second compartment.
    a, b = line[: len(line) // 2], line[len(line) // 2 :]
    assert len(a) == len(b)
    return priority(set(a) & set(b))


def compute_a(file: str) -> int:
    with open(file) as f:
        return sum(common_compartment_priority(line.strip()) for line in f)


def compute_b(file):
    with open(file) as f:
        lines = f.read().splitlines()
    # Every set of three lines in your list corresponds to a single group,
    # but each group can have a different badge item type.
    # the badge is the only item type carried by all three Elves
    iter_3_at_a_time = zip(*[iter(lines)] * 3)
    return sum(priority(set(a) & set(b) & set(c)) for a, b, c in iter_3_at_a_time)


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
