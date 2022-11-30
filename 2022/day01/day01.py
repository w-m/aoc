from funcy import print_durations
import numpy as np
import pandas as pd
import os.path
from collections import deque, Counter, defaultdict


def compute(file):
    yield None

    yield None


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
    run_expect("test_input.txt", None, None)
    run_expect("input.txt", None, None)
