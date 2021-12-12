from funcy import print_durations
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Path:
    """Keep a path through the graph and the count of elements"""

    path: [str]
    visited_any_lower_twice: bool = False

    def add_node(self, node: str):
        visited_twice = self.visited_any_lower_twice or (node.islower() and node in self.path)
        return Path(path=[*self.path, node], visited_any_lower_twice=visited_twice)


def read_graph(file):

    with open(file, "r") as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    G = defaultdict(set)

    for a, b in edges:
        G[a].add(b)
        G[b].add(a)

    return G


def valid_edge_visit_small_twice(b, cur_path):
    return not cur_path.visited_any_lower_twice


def find_path(graph, cur_path, paths, edge_validator=None):

    for b in graph[cur_path.path[-1]]:

        # once you leave the start cave, you may not return to it
        if b == "start":
            continue

        # once you reach the end cave, the path must end immediately
        if b == "end":
            paths.append([*cur_path.path, b])
            continue

        # big caves can be visited any number of times
        if b.isupper() or b not in cur_path.path or edge_validator and edge_validator(b, cur_path):
            new_path = cur_path.add_node(b)
            find_path(graph, new_path, paths, edge_validator)


def day12(file):
    graph = read_graph(file)

    small_once_paths = []
    find_path(graph, Path(path=["start"]), small_once_paths)
    yield len(small_once_paths)

    small_twice_paths = []
    find_path(graph, Path(path=["start"]), small_twice_paths, valid_edge_visit_small_twice)
    yield len(small_twice_paths)


@print_durations
def run_expect(file, result_a, result_b):

    a, b = day12(file)

    print(f"Day 12a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 12b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("test_input_a.txt", 10, 36)
    run_expect("test_input_b.txt", 19, 103)
    run_expect("test_input_c.txt", 226, 3509)
    run_expect("input.txt", 3421, 84870)
