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


def valid_edge(b, cur_path):

    # big caves can be visited any number of times
    if b.isupper():
        return True

    # once you leave the start cave, you may not return to it
    if b == "start":
        return False

    # not visited yet
    if b not in cur_path:
        return True

    lower_counter = Counter(node for node in cur_path if node.islower())

    if len(lower_counter) == sum(lower_counter.values()):
        return True

    # node_series = pd.Series(cur_path)
    # lower_vc = node_series[node_series.str.islower()].value_counts()

    # if (lower_vc > 1).any():
    #     return False

    return False


def find_path_visit_small_once(graph, cur_path, paths):

    for a, b in graph.edges(cur_path[-1:]):

        if b == "end":
            paths.append([*cur_path, b])
            continue

        if b.isupper() or b not in cur_path:
            new_path = [*cur_path, b]
            find_path_visit_small_once(graph, new_path, paths)


def find_path_visit_small_twice(graph, cur_path, paths):

    for a, b in graph.edges(cur_path[-1:]):

        # once you reach the end cave, the path must end immediately
        if b == "end":
            paths.append([*cur_path, b])
            continue

        if valid_edge(b, cur_path):
            new_path = [*cur_path, b]
            find_path_visit_small_twice(graph, new_path, paths)


@print_durations
def day12_a(file):

    graph = read_graph(file)

    paths = []
    find_path_visit_small_once(graph, ["start"], paths)

    return len(paths)


@print_durations
def day12_b(file):

    graph = read_graph(file)

    paths = []
    find_path_visit_small_twice(graph, ["start"], paths)

    return len(paths)


if __name__ == "__main__":
    test_aa, test_ab, test_ac = day12_a("test_input_a.txt"), day12_a("test_input_b.txt"), day12_a("test_input_c.txt")
    test_ba, test_bb, test_bc = day12_b("test_input_a.txt"), day12_b("test_input_b.txt"), day12_b("test_input_c.txt")
    solution_a = day12_a("input.txt")
    solution_b = day12_b("input.txt")

    print(f"Day 11a test a: {test_aa}")
    print(f"Day 11a test b: {test_ab}")
    print(f"Day 11a test c: {test_ac}")

    print(f"Day 11b test a: {test_ba}")
    print(f"Day 11b test b: {test_bb}")
    print(f"Day 11b test c: {test_bc}")

    print(f"Day 11a solution: {solution_a}")
    print(f"Day 11b solution: {solution_b}")

    assert test_aa == 10
    assert test_ab == 19
    assert test_ac == 226

    assert test_ba == 36
    assert test_bb == 103
    assert test_bc == 3509

    assert solution_a == 3421
    assert solution_b == 84870
