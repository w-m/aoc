from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
import pandas as pd
from copy import copy
from dataclasses import dataclass

# https://adventofcode.com/2022/day/7


class Dir(object):
    def __init__(self, name: str, children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.tostr()

    def tostr(self, level=0):
        return "\t" * level + self.name + "\n" + "\n".join(child.tostr(level + 1) for child in self.children)

    def add_child(self, node):
        self.children.append(node)

    def get_child_dir(self, dir_name):
        for child in self.children:
            if isinstance(child, Dir) and child.name == dir_name:
                return child
        dir = Dir(dir_name)
        self.add_child(dir)
        return dir

    def compute_a(self):
        # To begin, find all of the directories with a total size of at most 100000,
        # then calculate the sum of their total sizes.
        # In the example above, these directories are a and e;
        # the sum of their total sizes is 95437 (94853 + 584).
        # (As in this example, this process can count files more than once!)
        total_sum = 0
        if self.size <= 100000:
            total_sum += self.size
        for child in self.children:
            if isinstance(child, Dir):
                total_sum += child.compute_a()
        return total_sum

    def all_dirs(self):
        dirs = []
        for child in self.children:
            if isinstance(child, Dir):
                dirs.append(child)
                dirs.extend(child.all_dirs())
        return dirs

    @property
    def size(self):
        return sum(child.size for child in self.children)


@dataclass
class File(object):
    name: str
    size: int

    def tostr(self, level=0):
        return "\t" * level + self.name + " " + str(self.size)


@print_durations
def compute(file) -> Iterator[Optional[int]]:

    with open(file) as f:
        commands = [cmd.splitlines() for cmd in f.read().split("$ ")]

    cwd_stack = []

    root = Dir("/")

    for command in commands:
        if not len(command):
            continue

        # Within the terminal output, lines that begin with $ are commands you executed
        cmd = command[0].split()
        if cmd[0] == "cd":
            # cd .. moves out one level
            if cmd[1] == "..":
                cwd_stack.pop()
            # cd / switches the current directory to the outermost directory, /
            elif cmd[1] == "/":
                cwd_stack = [root]
            else:
                dir_name = cmd[1]
                dir = cwd_stack[-1].get_child_dir(dir_name)
                cwd_stack.append(dir)
        # ls means list
        elif cmd[0] == "ls":
            for ls_result in command[1:]:
                lsr = ls_result.split()
                # dir xyz means that the current directory contains a directory named xyz
                if lsr[0] == "dir":
                    dir_name = lsr[1]
                    # creates if it doesn't exist
                    cwd_stack[-1].get_child_dir(dir_name)
                else:
                    # 123 abc means that the current directory contains a file named abc with size 123
                    size = int(lsr[0])
                    name = lsr[1]
                    cwd_stack[-1].add_child(File(name, size))

    print(root)

    yield root.compute_a()

    # The total disk space available to the filesystem is 70000000
    space_available = 70000000
    # To run the update, you need unused space of at least 30000000
    required_space = 30000000

    cur_size = root.size
    need_to_free_up = cur_size - space_available + required_space
    # free up enough space

    # Find the smallest directory that, if deleted, would free up enough space on the filesystem
    # to run the update. What is the total size of that directory?

    smallest_size = space_available
    for dir in root.all_dirs():
        if dir.size < smallest_size and dir.size >= need_to_free_up:
            smallest_size = dir.size

    yield smallest_size


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
