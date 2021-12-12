from funcy import print_durations
from collections import defaultdict

# TODO remove edge to "start"
# TODO duplicate lower case nodes


def read_graph(file):

    with open(file, "r") as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    # {'start': 1, 'A': 2, 'b': 4, 'c': 8, 'd': 16, 'end': 32}
    nodes = {}

    # {1, 4, 8, 16, 32}
    lower_node_ids = set()

    node_id = 1

    for ab in edges:
        for node in ab:
            if node not in nodes:
                nodes[node] = node_id
                if node.islower():
                    lower_node_ids.add(node_id)
                node_id <<= 1

    G = defaultdict(set)

    for a, b in edges:
        G[nodes[a]].add(nodes[b])
        G[nodes[b]].add(nodes[a])

    return G, nodes, lower_node_ids


def count_paths(graph, node, visited, end_id, allow_single_visit, allow_second_visit=0, visited_any_twice=False):

    num_paths = 0

    for target in graph[node]:

        # once you reach the end cave, the path must end immediately
        if target == end_id:
            num_paths += 1
            continue

        if target & visited:

            if target & allow_single_visit:
                continue

            if visited_any_twice and target & allow_second_visit:
                continue

        num_paths += count_paths(
            graph, target, visited | target, end_id, allow_single_visit, allow_second_visit, visited_any_twice | (target & visited) & allow_second_visit
        )

    return num_paths


def day12(file):
    graph, node_lookup, lower_node_ids = read_graph(file)

    start_node_id = node_lookup["start"]

    allow_single_visit = 0
    for node_name, node_id in node_lookup.items():
        if node_name.islower():
            allow_single_visit |= node_id

    yield count_paths(graph, start_node_id, start_node_id, node_lookup["end"], allow_single_visit=allow_single_visit)

    allow_single_visit = node_lookup["start"] | node_lookup["end"]

    allow_second_visit = 0
    for node_name, node_id in node_lookup.items():
        if node_name == "start":
            continue
        if node_name == "end":
            continue
        if node_name.islower():
            allow_second_visit |= node_id
    yield count_paths(graph, start_node_id, start_node_id, node_lookup["end"], allow_single_visit=allow_single_visit, allow_second_visit=allow_second_visit)


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
