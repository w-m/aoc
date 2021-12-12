from funcy import print_durations
from collections import defaultdict


def read_graph(file):

    with open(file, "r") as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    # {'start': 1, 'A': 2, 'b': 3, 'c': 4, 'd': 5, 'end': 6}
    nodes = {}

    lower_node_ids = set()

    node_id = 1

    for ab in edges:
        for node in ab:
            if node not in nodes:
                nodes[node] = node_id
                if node.islower():
                    lower_node_ids.add(node_id)
                node_id += 1

    G = defaultdict(set)

    for a, b in edges:
        G[nodes[a]].add(nodes[b])
        G[nodes[b]].add(nodes[a])

    return G, nodes, lower_node_ids


def count_paths(graph, node, visited, start_id, end_id, lower_node_ids, allow_second_visit=False, visited_any_lower_twice=False):

    num_paths = 0

    for target in graph[node]:

        # once you leave the start cave, you may not return to it
        if target == start_id:
            continue

        # once you reach the end cave, the path must end immediately
        if target == end_id:
            num_paths += 1
            continue

        # big caves can be visited any number of times
        if target not in lower_node_ids or target not in visited or allow_second_visit and not visited_any_lower_twice:
            visited_twice = visited_any_lower_twice or (target in lower_node_ids and target in visited)
            num_paths += count_paths(graph, target, visited | {node}, start_id, end_id, lower_node_ids, allow_second_visit, visited_twice)

    return num_paths


def day12(file):
    graph, node_lookup, lower_node_ids = read_graph(file)

    start_node_id = node_lookup["start"]

    yield count_paths(graph, start_node_id, {start_node_id}, start_node_id, node_lookup["end"], lower_node_ids)
    yield count_paths(graph, start_node_id, {start_node_id}, start_node_id, node_lookup["end"], lower_node_ids, allow_second_visit=True)


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
