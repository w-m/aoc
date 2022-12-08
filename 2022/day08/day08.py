from funcy import print_durations
import os
import sys
from typing import List, Iterator, Optional
import pandas as pd
from copy import copy
import numpy as np
from collections import *

# https://adventofcode.com/2022/day/8


def iter_visible(arr, visible):
    col = np.zeros((arr.shape[0]), dtype=np.int32)
    col[:] = -1
    for i in range(arr.shape[1]):
        # visible: if col value is smaller than arr value, then it is visible
        visible[:, i] |= np.where(col < arr[:, i], 1, 0)
        col = np.max(arr[:, : i + 1], axis=1)

    return arr, visible


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        lines = list(map(list, f.read().splitlines()))

    arr = np.array(lines, dtype=np.int32)

    visible = np.zeros_like(arr, dtype=np.int32)

    arr, visible = iter_visible(arr, visible)
    arr = arr[:, ::-1]
    visible = visible[:, ::-1]
    arr, visible = iter_visible(arr, visible)
    arr = arr[::-1, :].T
    visible = visible[::-1, :].T
    arr, visible = iter_visible(arr, visible)
    arr = arr[:, ::-1]
    visible = visible[:, ::-1]
    arr, visible = iter_visible(arr, visible)
    arr = arr.T
    visible = visible.T

    yield visible.sum()

    with open(file) as f:
        lines = list(map(list, f.read().splitlines()))

    arr = np.array(lines, dtype=np.int32)

    score = np.zeros_like(arr, dtype=np.int32)

    def score_line(line):
        if line.sum() == 0:
            return len(line) - 1

        return np.argmax(line)

    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if y == 3 and x == 2:
                pass
            col = arr[:, x]
            row = arr[y, :]
            val = arr[y, x]
            cgt = col >= val
            rgt = row >= val
            cgt[y] = False
            rgt[x] = False
            right = score_line(rgt[x:])
            left = score_line(rgt[: x + 1][::-1])
            down = score_line(cgt[y:])
            up = score_line(cgt[: y + 1][::-1])
            score[y, x] = right * left * down * up

    yield score.max()


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
    run_expect("test_input.txt", 21, 8)
    run_expect("input.txt", 1785, -1)
