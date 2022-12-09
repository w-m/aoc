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

    Tx_upd = Tx + 1 if Tx < Hx else Tx - 1
    Ty_upd = Ty + 1 if Ty < Hy else Ty - 1
    
    # horizontal offset
    if xdiff > 0 and ydiff == 0:
        return Tx_upd, Ty
    
    # vertical offset
    if ydiff > 0 and xdiff == 0:
        return Tx, Ty_upd
    
    # diagonal offset
    return Tx_upd, Ty_upd

def test_tails_upd(Tx, Ty, Hx, Hy, expected_Tx, expected_Ty):
    assert update_tails(Tx, Ty, Hx, Hy) == (expected_Tx, expected_Ty)

def vis_visited(visited):
    minxs = min(x for x, y in visited)
    minys = min(y for x, y in visited)
    maxxs = max(x for x, y in visited)
    maxys = max(y for x, y in visited)
    vis = np.zeros((maxys - minys + 1, maxxs - minxs + 1), dtype=bool)
    for x, y in visited:
        vis[y - minys, x - minxs] = True
    
    print(np.array2string(vis[::-1], separator="", formatter={"bool": {0: " ", 1: "█"}.get}))

def simulate_rope(head_moves, rope_len):
    Txs = [0] * rope_len
    Tys = [0] * rope_len

    visited = {(Txs[-1], Tys[-1])}

    for head_move in head_moves:
        movement, steps = head_move.split()
        for i in range(int(steps)):
        
            match movement:
                case "R":
                    Txs[0] += 1
                case "L":
                    Txs[0] -= 1
                case "U":
                    Tys[0] += 1
                case "D":
                    Tys[0] -= 1
                
            for j in range(1, rope_len):
                Txs[j], Tys[j] = update_tails(Txs[j], Tys[j], Txs[j-1], Tys[j-1])
            visited.add((Txs[-1], Tys[-1]))
            
    return visited

@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        lines = f.read().splitlines()

    visited = simulate_rope(lines, 2)
    vis_visited(visited)
    yield len(visited)

    visited = simulate_rope(lines, 10)
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
