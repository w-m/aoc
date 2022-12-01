from funcy import print_durations
import os.path
from typing import List, Iterator

# https://adventofcode.com/2022/day/1

# The Elves take turns writing down the number of Calories contained by the various meals,
# snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates
# their own inventory from the previous Elf's inventory (if any) by a blank line.


@print_durations
def compute(file) -> Iterator[int]:
    with open(file, "r") as f:
        split_elves = f.read().split("\n\n")

    elf_calories: List[List[str]] = [elf.split("\n") for elf in split_elves]
    caloric_sums: List[int] = [sum(int(cal) for cal in elf) for elf in elf_calories]

    yield max(caloric_sums)

    yield sum(sorted(caloric_sums, reverse=True)[:3])


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
    run_expect("test_input.txt", 24000, 45000)
    run_expect("input.txt", 67016, 200116)
