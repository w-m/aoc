import os.path
from collections import *
from copy import copy
from typing import Iterator, List, Optional

import numpy as np
import pandas as pd
from funcy import print_durations
from dataclasses import dataclass

# https://adventofcode.com/2022/day/11


@dataclass
class Monkey:
    id: int
    items: List[int]
    operation: str
    div_by: int
    if_true: int
    if_false: int
    num_inspected: int = 0

    def turn(self):
        pass


def divisible(x, y):
    return x % y == 0


@print_durations
def compute_a(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        monkeys_lines = f.read().split("\n\n")

    # Sample monkey:
    # Monkey 0:
    #   Starting items: 79, 98
    #   Operation: new = old * 19
    #   Test: divisible by 23
    #     If true: throw to monkey 2
    #     If false: throw to monkey 3

    monkeys: Dict[int, Monkey] = {}

    for ml in monkeys_lines:
        lines = ml.split("\n")
        monkey_id = int(lines[0].split(" ")[1][:-1])
        starting_items = [int(x) for x in lines[1].split(":")[1].split(",")]
        operation = lines[2].split("=")[1].strip()
        div_by = int(lines[3].split(" ")[-1])
        if_true = int(lines[4].split("monkey")[1])
        if_false = int(lines[5].split("monkey")[1])
        monkeys[monkey_id] = Monkey(monkey_id, starting_items, operation, div_by, if_true, if_false)

    for round_id in range(20):
        print(f"Round {round_id}")

        for monkey_id, monkey in monkeys.items():
            print(f"Monkey {monkey_id} has {monkey.items}")

        for monkey_id, monkey in monkeys.items():

            if not monkey.items:
                continue

                # On a single monkey's turn, it inspects and throws all of the items it is holding

            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                monkey.num_inspected += 1
                old = item
                new = eval(monkey.operation)
                # After each monkey inspects an item but before it tests your worry level,
                # your relief that the monkey's inspection didn't damage the item causes
                # your worry level to be divided by three and rounded down to the nearest integer.
                worry_level = new // 3
                if divisible(worry_level, monkey.div_by):
                    monkeys[monkey.if_true].items.append(worry_level)
                else:
                    monkeys[monkey.if_false].items.append(worry_level)

    # you're going to have to focus on the two most active monkeys

    # Count the total number of times each monkey inspects items over 20 rounds

    # multiply together two most active monkeys after 20 rounds
    inspected = []
    for monkey_id, monkey in monkeys.items():
        print(f"Monkey {monkey_id} inspected {monkey.num_inspected} items")
        inspected.append(monkey.num_inspected)
    inspected.sort(reverse=True)

    return inspected[0] * inspected[1]


@print_durations
def compute_b(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        monkeys_lines = f.read().split("\n\n")

    # Sample monkey:
    # Monkey 0:
    #   Starting items: 79, 98
    #   Operation: new = old * 19
    #   Test: divisible by 23
    #     If true: throw to monkey 2
    #     If false: throw to monkey 3

    monkeys: Dict[int, Monkey] = {}

    for ml in monkeys_lines:
        lines = ml.split("\n")
        monkey_id = int(lines[0].split(" ")[1][:-1])
        starting_items = [int(x) for x in lines[1].split(":")[1].split(",")]
        operation = lines[2].split("=")[1].strip()
        div_by = int(lines[3].split(" ")[-1])
        if_true = int(lines[4].split("monkey")[1])
        if_false = int(lines[5].split("monkey")[1])
        monkeys[monkey_id] = Monkey(monkey_id, starting_items, operation, div_by, if_true, if_false)

    for round_id in range(10000):

        if round_id in [1, 20, 100] or round_id % 1000 == 0:
            print(f"Round {round_id}")
            div_by_tot = 1
            for monkey_id, monkey in monkeys.items():
                div_by_tot *= monkey.div_by
                print(f"Monkey {monkey_id} has {monkey.items}")

        for monkey_id, monkey in monkeys.items():

            if not monkey.items:
                continue

                # On a single monkey's turn, it inspects and throws all of the items it is holding

            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                monkey.num_inspected += 1
                old = item
                new = eval(monkey.operation)
                # After each monkey inspects an item but before it tests your worry level,
                # your relief that the monkey's inspection didn't damage the item causes
                # your worry level to be divided by three and rounded down to the nearest integer.
                # worry_level = new // 3
                worry_level = new % div_by_tot
                if divisible(worry_level, monkey.div_by):
                    monkeys[monkey.if_true].items.append(worry_level)
                else:
                    monkeys[monkey.if_false].items.append(worry_level)

    # you're going to have to focus on the two most active monkeys

    # Count the total number of times each monkey inspects items over 20 rounds

    # multiply together two most active monkeys after 20 rounds
    inspected = []
    for monkey_id, monkey in monkeys.items():
        print(f"Monkey {monkey_id} inspected {monkey.num_inspected} items")
        inspected.append(monkey.num_inspected)
    inspected.sort(reverse=True)

    return inspected[0] * inspected[1]


def compute(file) -> Iterator[Optional[int]]:
    return compute_a(file), compute_b(file)


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
    run_expect("test_input.txt", 10605, 2713310158)
    run_expect("input.txt", 54054, -1)
