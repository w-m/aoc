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

    floor = np.zeros((2, vent_lines[:, :, 0].max() + 1, vent_lines[:, :, 1].max() + 1), dtype=np.int64)

    for ((start_x, start_y), (stop_x, stop_y)) in vent_lines:

        if start_x == stop_x:
            if start_y <= stop_y:
                floor[:, start_y : stop_y + 1, start_x] += 1
            else:
                floor[:, start_y : stop_y - 1 : -1, start_x] += 1
        elif start_y == stop_y:
            if start_x <= stop_x:
                floor[:, start_y, start_x : stop_x + 1] += 1
            else:
                floor[:, start_y, start_x : stop_x - 1 : -1] += 1
        else:
            if start_x <= stop_x:
                xs = np.arange(start_x, stop_x + 1)
            else:
                xs = np.arange(start_x, stop_x - 1, -1)
            if start_y <= stop_y:
                ys = np.arange(start_y, stop_y + 1)
            else:
                ys = np.arange(start_y, stop_y - 1, -1)
            floor[1, ys, xs] += 1

    return (floor[0] > 1).sum(), (floor[1] > 1).sum()


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
