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
                folds.append(line.split()[-1].split("="))
            else:
                dots.append(line.split(","))

    dots = np.array(dots, dtype=int)

    return dots, folds


def day13(file):

    dots, folds = read_paper(file)

    paper = np.zeros((dots[:, 1].max() + 1, dots[:, 0].max() + 1), dtype=int)
    paper[dots[:, 1], dots[:, 0]] = 1
    np.set_printoptions(linewidth=100000)

    for fold_id, (axis, line) in enumerate(folds):

        line = int(line)

        if axis == "x":
            paper[:, :line] += paper[:, line + 1 :][:, ::-1]
            paper = paper[:, :line]
        else:
            if paper.shape[0] % 2 == 0:
                paper[1 : line + 1] += paper[line:][::-1]
                paper = paper[:line]
            else:
                paper[:line] += paper[line + 1 :][::-1]
                paper = paper[:line]

        if fold_id == 0:
            yield (paper > 0).sum()

    result = paper > 0
    rstr = np.where(result, "█", " ")

    for y in range(result.shape[0]):
        print("".join(rstr[y]))

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
