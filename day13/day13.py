from funcy import print_durations
import numpy as np


def read_paper(file):

    dots = []
    folds = []

    with open(file, "r") as f:
        for line in f:
            line = line.strip()

            if not len(line):
                continue
            if line.startswith("fold along"):
                axis, num = line.split()[-1].split("=")
                folds.append((axis, int(num)))
            else:
                dots.append(line.split(","))

    dots = np.array(dots, dtype=int)
    return dots, folds


def day13(file):
    dots, folds = read_paper(file)

    max_fold_x = 0
    max_fold_y = 0
    for axis, line in folds:
        if axis == "x":
            max_fold_x = max(max_fold_x, line)
        if axis == "y":
            max_fold_y = max(max_fold_y, line)

    paper = np.zeros((max_fold_y * 2 + 1, max_fold_x * 2 + 1), dtype=int)
    paper[dots[:, 1], dots[:, 0]] = 1

    for fold_id, (axis, line) in enumerate(folds):

        if axis == "x":
            paper = paper[:, :line] + paper[:, -1:line:-1]
        else:
            paper = paper[:line] + paper[-1:line:-1]

        if fold_id == 0:
            yield (paper > 0).sum()

    result = paper > 0
    print(np.array2string(result, separator="", formatter={"bool": {0: " ", 1: "█"}.get}))

    yield result.sum()


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
