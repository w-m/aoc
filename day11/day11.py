import numpy as np
import cv2
from funcy import print_durations
import itertools


def read_file(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(list(line.strip()))

    return np.array(data, dtype=int)


def step(octos):

    any_has_flashed = True

    has_flashed_this_step = np.zeros_like(octos, dtype=bool)

    kernel = np.ones((3, 3), np.uint8)

    # first, the energy level of each octopus increases by 1
    octos += 1

    while any_has_flashed:

        # then, any octopus with an energy level greater than 9 flashes
        flashing = octos > 9

        # an octopus can only flash at most once per step
        flashing &= ~has_flashed_this_step

        any_has_flashed = flashing.any()

        # this increases the energy level of all adjacent octopuses by 1
        # including octopuses that are diagonally adjacent

        # energy_increase = cv2.dilate(flashing.astype(np.uint8), kernel)

        energy_increase = cv2.filter2D(src=flashing.astype(np.uint8), ddepth=-1, kernel=kernel, borderType=cv2.BORDER_ISOLATED)

        octos += energy_increase

        # if this causes an octopus to have an energy level greater than 9, it also flashes
        # This process continues as long as new octopuses keep having their energy level increased beyond 9

        has_flashed_this_step |= flashing

    # finally, any octopus that flashed during this step has its energy level set to 0
    # as it used all of its energy to flash
    octos[has_flashed_this_step] = 0

    step_flashes = has_flashed_this_step.sum()

    return step_flashes


@print_durations
def day11(file):

    octos = read_file(file)

    total_flashes = 0

    for i in range(100):
        total_flashes += step(octos)

    yield total_flashes

    octos = read_file(file)
    for i in itertools.count(start=1):
        num_flashes = step(octos)
        if num_flashes == np.prod(octos.shape):
            yield i
            break


if __name__ == "__main__":
    test_a, test_b = day11("test_input.txt")
    solution_a, solution_b = day11("input.txt")

    print(f"Day 11a test: {test_a}")
    print(f"Day 11b test: {test_b}")

    print(f"Day 11a solution: {solution_a}")
    print(f"Day 11b solution: {solution_b}")

    assert test_a == 26397
    # assert test_b == 288957

    assert solution_a == 388713
    # assert solution_b == 3539961434
