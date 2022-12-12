import os.path
from collections import *
from copy import copy
from typing import Iterator, List, Optional

import numpy as np
import pandas as pd
from funcy import print_durations
import networkx as nx

# https://adventofcode.com/2022/day/12


def maze_to_val(maze_char):
    if maze_char == "S":
        return 0
    if maze_char == "E":
        return 25
    return ord(maze_char) - ord("a")


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    # a map of risk level throughout the cave
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(list(line.strip()))

    maze = np.array(data)

    graph = nx.grid_2d_graph(*maze.shape).to_directed()

    for u, v, data in graph.edges(data=True):
        diff = maze_to_val(maze[v[0], v[1]]) - maze_to_val(maze[u[0], u[1]])
        if diff > 1:
            data["step"] = 1000
        else:
            data["step"] = 1

    source = tuple(np.argwhere(maze == "S")[0])
    # find "E" in maze
    target = tuple(np.argwhere(maze == "E")[0])

    yield nx.dijkstra_path_length(graph, source, target, weight="step")

    # all points in maze with value "a"
    sources = [tuple(x) for x in np.argwhere(maze == "a")]
    sources.append(source)
    msd = nx.multi_source_dijkstra(graph, sources, target, weight="step", cutoff=1000)

    yield msd[0]


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
    run_expect("test_input.txt", 31, 29)
    run_expect("input.txt", 472, 465)
