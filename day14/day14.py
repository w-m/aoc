from funcy import print_durations
from itertools import pairwise
from collections import Counter
from copy import copy

# Puzzle: https://adventofcode.com/2021/day/14


def read_polymer(file):

    with open(file, "r") as f:
        polymer, rules = f.read().split("\n\n")

    # {('C', 'H'): 'B',
    #  ('H', 'H'): 'N',
    #  ('C', 'B'): 'H',
    #  ...
    # }
    rules = {tuple(ab): c for (ab, c) in (line.strip().split(" -> ") for line in rules.splitlines())}
    return polymer, rules


def insert_polymers(polymer, rules):

    new_polymer = []
    for pair in pairwise(polymer):
        first, _ = pair
        if pair in rules:
            new_polymer.extend([first, rules[pair]])
        else:
            new_polymer.append(first)

    # second part of pair is never inserted to not have duplication
    # --> need to append the last element again
    new_polymer.append(polymer[-1])

    return new_polymer


def count_polymer_insertion(paircount, rules):

    new_paircount = copy(paircount)

    for pair, insert_item in rules.items():

        first, second = pair
        cur_count = paircount[pair]

        new_paircount[pair] -= cur_count

        new_paircount[(first, insert_item)] += cur_count
        new_paircount[(insert_item, second)] += cur_count

    return new_paircount


def day14(file):

    polymer, rules = read_polymer(file)

    # puzzle part a: we can actually construct the polymer chain
    for i in range(10):
        polymer = insert_polymers(polymer, rules)
    most_common = Counter(polymer).most_common()

    # taking the quantity of the most common element and subtracting the quantity of the least common element
    yield most_common[0][1] - most_common[-1][1]

    # puzzle part b: it's getting too long, can only count occurrences

    polymer, rules = read_polymer(file)
    paircount = Counter(pairwise(polymer))

    for i in range(40):
        paircount = count_polymer_insertion(paircount, rules)

    lettercount = Counter()
    # count first letter of each pair
    for (a, b), count in paircount.items():
        lettercount[a] += count

    # and again, last element of chain
    lettercount[polymer[-1]] += 1

    most_common = lettercount.most_common()

    # taking the quantity of the most common element and subtracting the quantity of the least common element
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
