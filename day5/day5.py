import numpy as np
from funcy import print_durations


def read_vent_lines(file):
    with open(file, "r") as f:
        lines = f.readlines()

    vent_lines = [line.strip().split(" -> ") for line in lines]
    vent_lines = np.array([[start.split(","), stop.split(",")] for start, stop in vent_lines]).astype(dtype=np.int64)

    # dims: line, start/stop, x/y
    return vent_lines


@print_durations
def day5(file):

    vent_lines = read_vent_lines(file)

    # dims: 5a/5b (no diags, with diags), y, x
    floor = np.zeros((2, vent_lines[:, :, 1].max() + 1, vent_lines[:, :, 0].max() + 1), dtype=np.int64)

    for ((start_x, start_y), (stop_x, stop_y)) in vent_lines:

        direction_x = 1 if start_x <= stop_x else -1
        xs = np.arange(start_x, stop_x + direction_x, direction_x)

        direction_y = 1 if start_y <= stop_y else -1
        ys = np.arange(start_y, stop_y + direction_y, direction_y)

        if start_x == stop_x or start_y == stop_y:
            floor[0, ys, xs] += 1

        floor[1, ys, xs] += 1

    return (floor > 1).sum(axis=(1, 2))


if __name__ == "__main__":

    day5a_test, day5b_test = day5("test_input.txt")
    day5a_puzzle, day5b_puzzle = day5("input.txt")

    print(f"Day 5a: {day5a_test}")
    print(f"Day 5b: {day5b_test}")

    print(f"Day 5a: {day5a_puzzle}")
    print(f"Day 5b: {day5b_puzzle}")

    assert day5a_test == 5
    assert day5b_test == 12

    assert day5a_puzzle == 7269
    assert day5b_puzzle == 21140
