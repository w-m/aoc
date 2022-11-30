from funcy import print_durations
import pandas as pd
import numpy as np


def read_file(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(list(line.strip()))

    return np.array(data, dtype=int)


@print_durations
def day9(file):

    data = read_file(file)

    smaller_than_neighbor = np.ones_like(data, dtype=bool)

    # look south
    smaller_than_neighbor[:-1] &= data[:-1] < data[1:]

    # look north
    smaller_than_neighbor[1:] &= data[1:] < data[:-1]

    # look east
    smaller_than_neighbor[:, :-1] &= data[:, :-1] < data[:, 1:]

    # look west
    smaller_than_neighbor[:, 1:] &= data[:, 1:] < data[:, :-1]

    yield (data[smaller_than_neighbor] + 1).sum()

    basin_ids = np.arange(data.shape[0] * data.shape[1]).reshape(data.shape) + 1
    is_basin = data < 9
    basin_ids[~is_basin] = 0

    cur_sum = basin_ids.sum()

    while True:
        basin_ids[:-1] = np.maximum(basin_ids[:-1], basin_ids[1:])
        basin_ids[~is_basin] = 0

        basin_ids[:, :-1] = np.maximum(basin_ids[:, :-1], basin_ids[:, 1:])
        basin_ids[~is_basin] = 0

        basin_ids[1:] = np.maximum(basin_ids[:-1], basin_ids[1:])
        basin_ids[~is_basin] = 0

        basin_ids[:, 1:] = np.maximum(basin_ids[:, :-1], basin_ids[:, 1:])
        basin_ids[~is_basin] = 0

        new_sum = basin_ids.sum()

        if new_sum == cur_sum:
            break
        cur_sum = new_sum

    # ignore 0 (no-basin)
    basin_sizes = np.bincount(basin_ids.flatten())[1:]

    yield np.sort(basin_sizes)[-3:].prod()


if __name__ == "__main__":
    test_a, test_b = day9("test_input.txt")
    solution_a, solution_b = day9("input.txt")

    print(f"Day 9a test: {test_a}")
    print(f"Day 9b test: {test_b}")

    print(f"Day 9a solution: {solution_a}")
    print(f"Day 9b solution: {solution_b}")

    assert test_a == 15
    assert test_b == 1134

    assert solution_a == 452
    assert solution_b == 1263735
