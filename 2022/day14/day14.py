import itertools
import os.path
from typing import Iterator, List, Optional

import numpy as np
from funcy import print_durations

# https://adventofcode.com/2022/day/14


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def print_area(area):
    for row in area:
        print("".join(["#" if x == 1 else "." if x == 0 else "o" for x in row]))


def falling_sand(area, bounds):
    while True:
        # The sand is pouring into the cave from point 500,0. It immediately falls down one step
        sx = 500 - bounds[0]
        sy = 0

        # Sand is produced one unit at a time
        # and the next unit of sand is not produced until the previous unit of sand comes to rest
        while True:

            # would fall out of bounds
            if sy == area.shape[0] - 1:
                return

            if area[sy + 1, sx] == 0:
                # A unit of sand always falls down one step if possible
                sy += 1
            elif area[sy + 1, sx - 1] == 0:
                # If the tile immediately below is blocked (by rock or sand),
                # the unit of sand attempts to instead move diagonally one step down and to the left
                sy += 1
                sx -= 1
            elif area[sy + 1, sx + 1] == 0:
                # If that tile is blocked, the unit of sand attempts to instead
                # move diagonally one step down and to the right
                sy += 1
                sx += 1
            else:
                # If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves,
                # at which point the next unit of sand is created back at the source
                area[sy, sx] = 2

                if sy == 0:
                    # Sand not falling anymore, source of the sand becomes blocked
                    return

                break

        # print_area(area)


def read_walls(file):
    with open(file) as f:
        lines = f.read().splitlines()

    # x0, x1, y0, y1
    bounds = []

    walls = []
    for line in lines:
        # parse input walls:
        # x,y coordinates that form the shape of the path
        # x represents distance to the right and y represents distance down
        # 498,4 -> 498,6 -> 496,6
        # 503,4 -> 502,4 -> 502,9 -> 494,9
        segments = line.split(" -> ")
        wall = [tuple(map(int, segment.split(","))) for segment in segments]
        walls.append(wall)

        wall_bounds = [
            min(wall, key=lambda x: x[0])[0],
            max(wall, key=lambda x: x[0])[0] + 1,
            min(wall, key=lambda x: x[1])[1],
            max(wall, key=lambda x: x[1])[1] + 1,
        ]

        if bounds == []:
            bounds = wall_bounds
        else:
            bounds = [
                min(bounds[0], wall_bounds[0]),
                max(bounds[1], wall_bounds[1]),
                min(bounds[2], wall_bounds[2]),
                max(bounds[3], wall_bounds[3]),
            ]

    return walls, bounds


def gen_area(walls, bounds):

    # 0: empty, 1: wall, 2: sand
    area = np.zeros((bounds[3] - bounds[2], bounds[1] - bounds[0]), dtype=int)

    for segment_list in walls:
        for (x0, y0), (x1, y1) in pairwise(segment_list):
            xs, xe = sorted([x0, x1])
            ys, ye = sorted([y0, y1])
            area[
                ys - bounds[2] : ye - bounds[2] + 1,
                xs - bounds[0] : xe - bounds[0] + 1,
            ] = 1

    return area


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    walls, bounds = read_walls(file)

    # The sand is pouring into the cave from point 500,0
    bounds[0] -= 1  # x0
    bounds[1] += 1  # x1
    bounds[2] = 0  # y0
    bounds[3] += 1  # y1

    area = gen_area(walls, bounds)
    falling_sand(area, bounds)

    yield np.count_nonzero(area == 2)

    height = area.shape[0]

    # sand falls into triangle before it comes to rest,
    # -> grow bounds to include the triangle
    bounds[0] = 500 - (height + 1)  # x0
    bounds[1] = 500 + (height + 1)  # x1

    # source
    bounds[2] = 0  # y0

    bounds[3] = height + 1  # floor

    area = gen_area(walls, bounds)

    # assume the floor is an infinite horizontal line
    # with a y coordinate equal to two plus the highest y coordinate of any point in your scan
    area[bounds[3] - 1, :] = 1

    falling_sand(area, bounds)
    # print_area(area)

    yield np.count_nonzero(area == 2)


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
    run_expect("test_input.txt", 24, 93)
    run_expect("input.txt", 755, 29805)
