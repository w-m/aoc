from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
from collections import deque

# https://adventofcode.com/2022/day/6


def find_start_marker(line: str, unique_consecutive_chars: int) -> int:

    # The device will send your subroutine a datastream buffer (your puzzle input)

    # In the protocol being used by the Elves, the start of a packet is indicated
    # by a sequence of four characters that are all different.

    # report the number of characters from the beginning
    # of the buffer to the end of the first such four-character marker.

    deq = deque([], maxlen=unique_consecutive_chars)
    for i, char in enumerate(line):
        deq.append(char)
        if len(set(deq)) == unique_consecutive_chars:
            return i + 1
    assert False


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        line = f.read().strip()

    # start of packet marker
    yield find_start_marker(line, 4)

    # start of message marker
    yield find_start_marker(line, 14)


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
