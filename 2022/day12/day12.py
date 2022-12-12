import os.path
from typing import Iterator, List, Optional

import networkx as nx
import numpy as np
from funcy import print_durations

# https://adventofcode.com/2022/day/12


def maze_to_val(maze_char):
    if maze_char == "S":
        return 0
    if maze_char == "E":
        return 25
    return ord(maze_char) - ord("a")


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file, "r") as f:
        maze = np.array([list(x) for x in f.read().splitlines()])

    graph = nx.grid_2d_graph(*maze.shape).to_directed()

    too_steep = set()
    for u, v, _ in graph.edges(data=True):
        diff = maze_to_val(maze[v[0], v[1]]) - maze_to_val(maze[u[0], u[1]])
        if diff > 1:
            too_steep.add((u, v))

    graph.remove_edges_from(too_steep)

    source = tuple(np.argwhere(maze == "S")[0])
    target = tuple(np.argwhere(maze == "E")[0])

    s_t_len = nx.shortest_path_length(graph, source, target)
    yield s_t_len

    sources = [tuple(x) for x in np.argwhere(maze == "a")]
    sources.append(source)
    msd = nx.multi_source_dijkstra(graph, sources, target, cutoff=s_t_len)

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
