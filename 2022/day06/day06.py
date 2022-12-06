from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
from collections import deque

# https://adventofcode.com/2022/day/6


def read_single_line(file) -> str:
    with open(file) as f:
        return f.read().strip()


def find_start_marker(datastream: str, unique_consecutive_chars: int) -> int:

    # The device will send your subroutine a datastream buffer (your puzzle input)

    # In the protocol being used by the Elves, the start of a packet is indicated
    # by a sequence of four characters that are all different.

    # report the number of characters from the beginning
    # of the buffer to the end of the first such four-character marker.

    deq = deque([], maxlen=unique_consecutive_chars)
    for i, char in enumerate(datastream):
        deq.append(char)
        if len(set(deq)) == unique_consecutive_chars:
            return i + 1
    assert False


@print_durations
def compute(datastream) -> Iterator[Optional[int]]:

    # start of packet marker
    yield find_start_marker(datastream, 4)

    # start of message marker
    yield find_start_marker(datastream, 14)


@print_durations
def run_expect(datastream, result_a, result_b):
    a, b = compute(datastream)
    print(f"{datastream[:21]}...: {a}")
    assert a == result_a

    if result_b:
        print(f"{datastream[:21]}...: {b}")
        assert b == result_b


if __name__ == "__main__":
    run_expect("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23)
    run_expect("nppdvjthqldpwncqszvftbrmjlhg", 6, 23)
    run_expect("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29)
    run_expect("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26)
    run_expect(read_single_line("test_input.txt"), 7, 19)
    run_expect(read_single_line("input.txt"), 1275, 3605)
