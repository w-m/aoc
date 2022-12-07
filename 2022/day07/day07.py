from funcy import print_durations
import os.path
from typing import List, Iterator, Optional
from dataclasses import dataclass, field

# https://adventofcode.com/2022/day/7


@dataclass
class Dir(object):
    name: str
    children: List = field(default_factory=lambda: [])

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

    def sum_directories_100k(self):
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
                total_sum += child.sum_directories_100k()
        return total_sum

    def smallest_dir_with_min_size(self, size):
        if self.size < size:
            return None

        smallest = self
        for child in self.children:
            if isinstance(child, Dir):
                child_smallest = child.smallest_dir_with_min_size(size)
                if child_smallest is not None:
                    if smallest is None or child_smallest.size < smallest.size:
                        smallest = child_smallest
        return smallest

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
        execs = [cmd.splitlines() for cmd in f.read().split("$ ")]

    cwd_stack: List[Dir] = []

    root = Dir("/")

    for exec in execs:
        if not len(exec):
            continue

        call, *output = exec

        # Within the terminal output, lines that begin with $ are commands you executed
        cmd, *params = call.split()
        if cmd == "cd":
            # cd .. moves out one level
            if params[0] == "..":
                cwd_stack.pop()
            # cd / switches the current directory to the outermost directory, /
            elif params[0] == "/":
                cwd_stack = [root]
            else:
                dir_name = params[0]
                dir = cwd_stack[-1].get_child_dir(dir_name)
                cwd_stack.append(dir)
        elif cmd == "ls":
            for ls_line in output:
                ls_split = ls_line.split()
                # dir xyz means that the current directory contains a directory named xyz
                if ls_split[0] == "dir":
                    dir_name = ls_split[1]
                    # creates if it doesn't exist
                    cwd_stack[-1].get_child_dir(dir_name)
                else:
                    # 123 abc means that the current directory contains a file named abc with size 123
                    size = int(ls_split[0])
                    name = ls_split[1]
                    cwd_stack[-1].add_child(File(name, size))

    yield root.sum_directories_100k()

    # The total disk space available to the filesystem is 70000000
    space_available = 70000000
    # To run the update, you need unused space of at least 30000000
    required_space = 30000000
    need_to_free_up = root.size - space_available + required_space

    # Find the smallest directory that, if deleted, would free up enough space on the filesystem
    # to run the update. What is the total size of that directory?
    yield root.smallest_dir_with_min_size(need_to_free_up).size


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
