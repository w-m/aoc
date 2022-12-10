import os.path
from collections import *
from copy import copy
from typing import Iterator, List, Optional

import numpy as np
import pandas as pd
from funcy import print_durations

# https://adventofcode.com/2022/day/10


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        lines = f.read().splitlines()
        
    ops = []
    noop = lambda x: x
        
    for line in lines:
        match line.split():
            case ["noop"]:
                ops.append(noop)
            case "addx", val:
                # addx takes two cycles
                ops.append(noop)
                ops.append(lambda x, ival=int(val): x + ival)
            case _:
                assert False
                
    xval = 1
    signal = 0
    crt = ""
    for cycle, op in enumerate(ops, start=1):

        if (cycle - 20) % 40 == 0:
            signal += cycle * xval
        
        crt_idx = (cycle - 1) % 40
        if xval >= crt_idx - 1 and xval <= crt_idx + 1:
            crt += "█"
        else:
            crt += " "
        
        if cycle % 40 == 0:
            crt += "\n"

        xval = op(xval)

    yield signal
    
    print(crt)
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
    run_expect("test_input.txt", 13140, None)
    run_expect("input.txt", 13760, None)
