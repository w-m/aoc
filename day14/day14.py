from funcy import print_durations
from itertools import pairwise
from collections import Counter
from copy import copy


def read_polymer(file):

    with open(file, "r") as f:
        polymer, rules = f.read().split("\n\n")

    rules = {tuple(ab): c for (ab, c) in [line.strip().split(" -> ") for line in rules.splitlines()]}
    return polymer, rules


def step(polymer, rules):

    new_polymer = []
    for (a, b) in pairwise(polymer):
        if (a, b) in rules:
            new_polymer.extend([a, rules[(a, b)]])
        else:
            new_polymer.append(a)

    new_polymer.append(polymer[-1])

    return new_polymer


def step_count(paircount, rules):

    new_paircount = copy(paircount)

    for (pair_a, pair_b), insert in rules.items():

        cur_count = paircount[(pair_a, pair_b)]
        new_paircount[(pair_a, pair_b)] -= cur_count

        new_paircount[(pair_a, insert)] += paircount[(pair_a, pair_b)]
        new_paircount[(insert, pair_b)] += paircount[(pair_a, pair_b)]

    return new_paircount


def day14(file):

    polymer, rules = read_polymer(file)

    for i in range(10):
        polymer = step(polymer, rules)
    most_common = Counter(polymer).most_common()
    yield most_common[0][1] - most_common[-1][1]

    polymer, rules = read_polymer(file)
    paircount = Counter(pairwise(polymer))

    for i in range(40):
        paircount = step_count(paircount, rules)

    lettercount = Counter()
    for (a, b), count in paircount.items():
        lettercount[a] += count

    lettercount[polymer[-1]] += 1

    most_common = lettercount.most_common()
    yield most_common[0][1] - most_common[-1][1]


@print_durations
def run_expect(file, result_a, result_b):

    a, b = day14(file)

    print(f"Day 14a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 14b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("test_input.txt", 1588, 2188189693529)
    run_expect("input.txt", 3587, 3906445077999)
