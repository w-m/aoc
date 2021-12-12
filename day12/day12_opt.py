from funcy import print_durations
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Path:
    visited: {str}
    visited_any_lower_twice: bool = False

    def add_node(self, node: str):
        visited_twice = self.visited_any_lower_twice or (node.islower() and node in self.visited)
        return Path(visited={*self.visited, node}, visited_any_lower_twice=visited_twice)


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


def count_paths(graph, node, cur_path, edge_validator=None):

    num_paths = 0

    for target in graph[node]:

        # once you leave the start cave, you may not return to it
        if target == "start":
            continue

        # once you reach the end cave, the path must end immediately
        if target == "end":
            num_paths += 1
            continue

        # big caves can be visited any number of times
        if target.isupper() or target not in cur_path.visited or edge_validator and edge_validator(target, cur_path):
            new_path = cur_path.add_node(target)
            num_paths += count_paths(graph, target, new_path, edge_validator)

    return num_paths


def day12(file):
    graph = read_graph(file)

    yield count_paths(graph, "start", Path(visited={"start"}))

    yield count_paths(graph, "start", Path(visited={"start"}), valid_edge_visit_small_twice)


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
