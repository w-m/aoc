from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd
from copy import copy

# https://adventofcode.com/2022/day/5


def compute_a(stacks, movelines) -> str:

    for moveline in movelines:
        # parse numbers from strings like "move 1 from 2 to 1"
        _, how_many, _, source, _, target = moveline.split()
        for i in range(int(how_many)):
            stacks[int(target) - 1].append(stacks[int(source) - 1].pop())

    return "".join(stack[-1] for stack in stacks)


def compute_b(stacks, movelines):

    for moveline in movelines:
        # parse numbers from strings like "move 1 from 2 to 1"
        _, how_many, _, source, _, target = moveline.split()

        elems_to_move = []
        for i in range(int(how_many)):
            elems_to_move.append(stacks[int(source) - 1].pop())

        stacks[int(target) - 1].extend(elems_to_move[::-1])

    return "".join(stack[-1] for stack in stacks)


def read_file(file):
    with open(file) as f:
        stacklines, movelines = f.read().split("\n\n")

    stacklines = stacklines.splitlines()[::-1]
    num_stacks = len(stacklines[0][1::4])
    stacks = [[] for _ in range(num_stacks)]
    for line in stacklines[1:]:
        stack_content = line[1::4]
        for i, stack in enumerate(stack_content):
            if stack != " ":
                stacks[i].append(stack)

    movelines = movelines.splitlines()

    return stacks, movelines


@print_durations
def compute(file) -> Iterator[Optional[str]]:

    yield compute_a(*read_file(file))
    yield compute_b(*read_file(file))


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
    run_expect("test_input.txt", "CMZ", "MCD")
    run_expect("input.txt", "TLNGFGMFN", "FGLQJCMBD")
