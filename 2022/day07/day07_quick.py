from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
from collections import *

# https://adventofcode.com/2022/day/7

# Reimplementing the quicker solutions found on Reddit
# Keep track of cwd with the cd commands
# Ignore ls and file names, just keep global track of directory sizes
# -> breaks if `ls` is called multiple times in the same directory
#    but so would my initial solution (adding files to the childrens list again)

@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        lines = f.readlines()

    cwd = []
    
    dirs = defaultdict(int)
    
    for line in lines:
        match line.split():
            case "$", "cd", "/":
                cwd = [""]
            case "$", "cd", "..":
                cwd.pop()
            case "$", "cd", dir:
                cwd.append(dir)
            case "$", "ls":
                pass
            case "dir", dir_name:
                pass
            case size, file_name:
                for i in range(len(cwd)):
                    dirs["/".join(cwd[:i+1])] += int(size)

    yield sum(val for val in dirs.values() if val <= 100000)
    yield min(val for val in dirs.values() if val >= 30000000 - (70000000 - dirs[""]))


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
    run_expect("test_input.txt", 95437, 24933642)
    run_expect("input.txt", 1086293, 366028)
