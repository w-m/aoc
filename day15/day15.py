from funcy import print_durations
import numpy as np
import networkx as nx

# Puzzle: https://adventofcode.com/2021/day/15


def read_maze(file):

    # a map of risk level throughout the cave
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(list(line.strip()))

    return np.array(data, dtype=int)


def supersize_maze(maze):

    offsets = np.mgrid[:5, :5].sum(axis=0)
    offsets = np.repeat(offsets, maze.shape[0], axis=0)
    offsets = np.repeat(offsets, maze.shape[1], axis=1)

    maze5x = np.tile(maze, (5, 5))
    maze5x += offsets

    maze5x[maze5x > 9] %= 9

    return maze5x


def risk_shortest_path(maze):
    graph = nx.grid_2d_graph(*maze.shape).to_directed()

    for y in range(maze.shape[0]):
        for x in range(maze.shape[1]):
            for edge in graph.in_edges((y, x)):
                graph.edges[edge]["risk"] = maze[y, x]

    # What is the lowest total risk of any path from the top left to the bottom right?
    path = nx.shortest_path(graph, source=(0, 0), target=(maze.shape[0] - 1, maze.shape[1] - 1), weight="risk")
    return nx.classes.function.path_weight(graph, path, "risk")


def day15(file):

    maze = read_maze(file)
    yield risk_shortest_path(maze)

    yield risk_shortest_path(supersize_maze(maze))


@print_durations
def run_expect(file, result_a, result_b):

    a, b = day15(file)

    print(f"Day 15a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 15b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("test_input.txt", 40, 315)
    run_expect("input.txt", 595, 2914)
