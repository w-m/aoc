from funcy import print_durations
import numpy as np
from io import StringIO


def read_paper(file):

    with open(file, "r") as f:
        dotstr, foldstr = f.read().split("\n\n")

    # [('y', 7), ('x', 5)]
    folds = np.loadtxt(StringIO(foldstr), dtype="str")[:, -1]
    folds = [(axis, int(num)) for axis, num in np.char.split(folds, "=")]

    # array([[ 6, 10],
    #         ...
    #        [ 9,  0]])
    dots = np.loadtxt(StringIO(dotstr), dtype=int, delimiter=",")
    return dots, folds


def day13(file):
    dots, folds = read_paper(file)

    max_fold_x = max(num for axis, num in folds if axis == "x")
    max_fold_y = max(num for axis, num in folds if axis == "y")

    # make twice as big as the largest fold in each dimension
    paper = np.zeros((max_fold_y * 2 + 1, max_fold_x * 2 + 1), dtype=bool)

    # draw dots
    paper[dots[:, 1], dots[:, 0]] = True

    for fold_id, (axis, line) in enumerate(folds):

        if axis == "x":
            paper = paper[:, :line] + paper[:, -1:line:-1]
        else:
            paper = paper[:line] + paper[-1:line:-1]

        if fold_id == 0:
            yield paper.sum()

    print(np.array2string(paper, separator="", formatter={"bool": {0: " ", 1: "█"}.get}))

    yield paper.sum()


@print_durations
def run_expect(file, result_a, result_b):

    a, b = day13(file)

    print(f"Day 13a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 13b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("test_input.txt", 17, 16)
    run_expect("input.txt", 827, 104)
