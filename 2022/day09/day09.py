from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd
from copy import copy
import numpy as np
from collections import *

# https://adventofcode.com/2022/day/09

def update_tails(Tx, Ty, Hx, Hy):

    xdiff = abs(Tx - Hx)
    ydiff = abs(Ty - Hy)
   
    if xdiff <= 1 and ydiff <= 1:
        return Tx, Ty
    
    if xdiff > 0 and ydiff == 0:
        if Tx < Hx:
            Tx += 1
        else:
            Tx -= 1
    elif ydiff > 0 and xdiff == 0:
        if Ty < Hy:
            Ty += 1
        else:
            Ty -= 1
    else:
        if Tx < Hx:
            Tx += 1
        else:
            Tx -= 1
        if Ty < Hy:
            Ty += 1
        else:
            Ty -= 1

    return Tx, Ty

def test_tails_upd(Tx, Ty, Hx, Hy, expected_Tx, expected_Ty):
    assert update_tails(Tx, Ty, Hx, Hy) == (expected_Tx, expected_Ty)

def vis_visited(visited):
    minxs = min(x for x, y in visited)
    minys = min(y for x, y in visited)
    maxxs = max(x for x, y in visited)
    maxys = max(y for x, y in visited)
    vis = np.zeros((maxys - minys + 1, maxxs - minxs + 1), dtype=np.int8)
    for x, y in visited:
        vis[y - minys, x - minxs] = 1
    
    print(vis[::-1])

@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        lines = f.read().splitlines()

    Hx, Hy = 0, 0
    Tx, Ty = 0, 0

    visited = {(Tx, Ty)}

    for line in lines:
        movement, steps = line.split()
        for i in range(int(steps)):
            match movement:
                case "R":
                    Hx += 1
                case "L":
                    Hx -= 1
                case "U":
                    Hy += 1
                case "D":
                    Hy -= 1

            Tx, Ty = update_tails(Tx, Ty, Hx, Hy)
            visited.add((Tx, Ty))

    vis_visited(visited)
    yield len(visited)

    Hx, Hy = 0, 0
    Txs = [0] * 9
    Tys = [0] * 9

    visited = {(Txs[-1], Tys[-1])}

    for line in lines:
        movement, steps = line.split()
        for i in range(int(steps)):
        
            match movement:
                case "R":
                    Hx += 1
                case "L":
                    Hx -= 1
                case "U":
                    Hy += 1
                case "D":
                    Hy -= 1
                
            Txs[0], Tys[0] = update_tails(Txs[0], Tys[0], Hx, Hy)
            for j in range(1, 9):
                Txs[j], Tys[j] = update_tails(Txs[j], Tys[j], Txs[j-1], Tys[j-1])
            visited.add((Txs[-1], Tys[-1]))

    vis_visited(visited)
    yield len(visited)


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
    test_tails_upd(0, 0, 1, 0, 0, 0)
    test_tails_upd(0, 0, 2, 0, 1, 0)
    
    test_tails_upd(0, 0, 1, 1, 0, 0)
    test_tails_upd(0, 0, 1, 2, 1, 1)
    run_expect("test_input.txt", 13, 1)
    run_expect("test_input_2.txt", 88, 36)
    run_expect("input.txt", 5619, 2376)
