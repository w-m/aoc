from funcy import print_durations
import networkx as nx
from collections import Counter


def read_graph(file):

    with open(file, "r") as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    nodes = {node for ab in edges for node in ab}

    G = nx.Graph()
    for node in nodes:
        # not used currently
        size = "big" if node.isupper() else "small"
        G.add_node(node, size=size)

    G.add_edges_from(edges)

    return G


def valid_edge_visit_small_twice(b, cur_path):
    lower_counter = Counter(node for node in cur_path if node.islower())

    if len(lower_counter) == sum(lower_counter.values()):
        return True

    return False


def find_path(graph, cur_path, paths, edge_validator=None):

    for a, b in graph.edges(cur_path[-1:]):

        # once you leave the start cave, you may not return to it
        if b == "start":
            continue

        # once you reach the end cave, the path must end immediately
        if b == "end":
            paths.append([*cur_path, b])
            continue

        # big caves can be visited any number of times
        if b.isupper() or b not in cur_path or edge_validator and edge_validator(b, cur_path):
            new_path = [*cur_path, b]
            find_path(graph, new_path, paths, edge_validator)


def day12(file):
    graph = read_graph(file)
    small_once_paths = []
    find_path(graph, ["start"], small_once_paths)
    yield len(small_once_paths)

    small_twice_paths = []
    find_path(graph, ["start"], small_twice_paths, valid_edge_visit_small_twice)
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
