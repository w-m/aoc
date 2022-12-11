import os.path
from typing import Iterator, List, Optional, Dict

from funcy import print_durations
from dataclasses import dataclass
from copy import deepcopy
from math import lcm
from functools import lru_cache

# https://adventofcode.com/2022/day/11


@dataclass
class Monkey:
    id: int
    items: List[int]
    operation: str
    div_by: int
    if_true: int
    if_false: int

    def __hash__(self):
        return self.id + sum(self.items) + hash(self.operation) + self.div_by + self.if_true + self.if_false


@dataclass
class Monkeys:
    monkeys: List[Monkey]

    def __hash__(self):
        return sum(hash(monkey) for monkey in self.monkeys)

    def __iter__(self):
        return iter(self.monkeys)

    def __getitem__(self, key):
        return self.monkeys[key]


@print_durations
def monkeys_round(monkeys: Monkeys, num_rounds, worry_reducer) -> int:

    inspected = [0 for _ in monkeys]

    for round_id in range(num_rounds):
        monkeys, newly_inspected = monkeys_throw_items(monkeys, worry_reducer)
        for monkey_id, num_inspected in enumerate(newly_inspected):
            inspected[monkey_id] += num_inspected

    # you're going to have to focus on the two most active monkeys
    # Count the total number of times each monkey inspects items
    inspected.sort(reverse=True)

    return inspected[0] * inspected[1]


# memoize
# @lru_cache(maxsize=None)
def monkeys_throw_items(monkeys, worry_reducer):

    inspected = [0 for _ in monkeys]

    for monkey_id, monkey in enumerate(monkeys):
        if not monkey.items:
            continue

            # On a single monkey's turn, it inspects and throws all of the items it is holding
        while len(monkey.items) > 0:
            item = monkey.items.pop(0)
            inspected[monkey_id] += 1
            old = item
            new = eval(monkey.operation)
            worry_level = worry_reducer(new)
            if worry_level % monkey.div_by == 0:
                monkeys[monkey.if_true].items.append(worry_level)
            else:
                monkeys[monkey.if_false].items.append(worry_level)

    return monkeys, inspected


def compute(file) -> Iterator[Optional[int]]:

    monkeys: Monkeys = parse_monkey_def(file)

    # After each monkey inspects an item but before it tests your worry level,
    # your relief that the monkey's inspection didn't damage the item causes
    # your worry level to be divided by three and rounded down to the nearest integer.
    yield monkeys_round(deepcopy(monkeys), 20, lambda worry_level: worry_level // 3)

    # Worry levels are no longer divided by three after each item is inspected;
    # you'll need to find another way to keep your worry levels manageable
    div_by_tot = lcm(*(monkey.div_by for monkey in monkeys))
    yield monkeys_round(monkeys, 10000, lambda x: x % div_by_tot)


def parse_monkey_def(file) -> Monkeys:
    with open(file) as f:
        monkeys_lines = f.read().split("\n\n")

    # Sample monkey:
    # Monkey 0:
    #   Starting items: 79, 98
    #   Operation: new = old * 19
    #   Test: divisible by 23
    #     If true: throw to monkey 2
    #     If false: throw to monkey 3

    monkeys: List[Monkey] = []

    for monkey_id, monkey_lines in enumerate(monkeys_lines):
        lines = monkey_lines.split("\n")
        assert lines[0] == f"Monkey {monkey_id}:"
        starting_items = [int(x) for x in lines[1].split(":")[1].split(",")]
        operation = lines[2].split("Operation: new =")[1].strip()
        div_by = int(lines[3].split("Test: divisible by")[1])
        if_true = int(lines[4].split("monkey")[1])
        if_false = int(lines[5].split("monkey")[1])
        monkeys.append(Monkey(monkey_id, starting_items, operation, div_by, if_true, if_false))
    return Monkeys(monkeys)


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
    run_expect("input.txt", 54054, 14314925001)
