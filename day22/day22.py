from funcy import print_durations
import numpy as np
from itertools import pairwise
import itertools
from dataclasses import dataclass
from tqdm.contrib import tzip

# Puzzle: https://adventofcode.com/2021/day/22

# reactor core is made up of a large 3-dimensional grid
# made up entirely of cubes, one cube per integer 3-dimensional coordinate (x,y,z)
# To reboot the reactor, you just need to set all of the cubes to either on or off by
# following a list of reboot steps (your puzzle input), e.g.:
#
#     on x=10..12,y=10..12,z=10..12
#     on x=11..13,y=11..13,z=11..13
#     off x=9..11,y=9..11,z=9..11
#     on x=10..10,y=10..10,z=10..10
#
# solution:
# - identify unique xs, ys and zs
# - map x->xs, y->ys, z->zs
# - write the steps into a grid
# - when counting the "on" cubes in the grid, multiply with their true size


def read_reboot_steps(file):

    commands = []
    coords = []

    with open(file, "r") as f:
        for line in f:
            onoff, coords_seg = line.strip().split(" ")
            commands.append(onoff == "on")

            steps_xyz = []
            for arg in coords_seg.split(","):
                begin, end = arg[2:].split("..")
                # note: endrange +1 to mark upper end of range (next coordinate)
                steps_xyz.append((int(begin), int(end) + 1))
            coords.append(steps_xyz)

    return np.array(commands), np.array(coords)


def count_active_cubes(commands, coords_list):

    xs = coords_list[:, 0, :]
    ys = coords_list[:, 1, :]
    zs = coords_list[:, 2, :]

    xuq, xinv = np.unique(xs, return_inverse=True)
    yuq, yinv = np.unique(ys, return_inverse=True)
    zuq, zinv = np.unique(zs, return_inverse=True)

    xsize = np.diff(xuq)
    ysize = np.diff(yuq)
    zsize = np.diff(zuq)

    coords_mapped = np.zeros_like(coords_list)
    coords_mapped[:, 0, :] = xinv.reshape(xs.shape)
    coords_mapped[:, 1, :] = yinv.reshape(ys.shape)
    coords_mapped[:, 2, :] = zinv.reshape(zs.shape)

    reactor = np.zeros((len(xuq), len(yuq), len(zuq)), dtype=bool)

    for command, coords in zip(commands, coords_mapped):
        reactor[coords[0, 0] : coords[0, 1], coords[1, 0] : coords[1, 1], coords[2, 0] : coords[2, 1]] = command

    sum = 0

    for x, y, z in tzip(*np.nonzero(reactor)):
        sum += xsize[x] * ysize[y] * zsize[z]

    return sum


def day22(file):

    commands, coords_list = read_reboot_steps(file)

    # day 22a: ignore cubes outside [-50, 50]
    commands_50, coords_list_50 = list(
        zip(
            *[
                (command, coords)
                for (command, coords) in zip(commands, coords_list)
                # up to coordinates 50 -> [:51]
                if (coords.min() >= -50) and (coords.max() <= 51)
            ]
        )
    )
    # day 22a
    yield count_active_cubes(commands_50, np.array(coords_list_50))

    # day 22b: full grid
    yield count_active_cubes(commands, coords_list)


@print_durations
def run_expect(file, result_a, result_b):
    a, b = day22(file)
    print(f"Day 22a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 22b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("tiny_input.txt", 39, 39)
    run_expect("test_input.txt", 590784, None)
    run_expect("test_input_b.txt", 474140, 2758514936282235)
    run_expect("input.txt", 658691, -1)
