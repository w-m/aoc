from funcy import print_durations
from collections import defaultdict


def read_graph(file):

    with open(file, "r") as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    G = defaultdict(set)

    for a, b in edges:
        G[a].add(b)
        G[b].add(a)

    return G


def count_paths(graph, node, visited, allow_second_visit=False, visited_any_lower_twice=False):

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
        if target.isupper() or target not in visited or allow_second_visit and not visited_any_lower_twice:
            visited_twice = visited_any_lower_twice or (target.islower() and target in visited)
            num_paths += count_paths(graph, target, visited | {node}, allow_second_visit, visited_twice)

    return num_paths


def day12(file):
    graph = read_graph(file)

    yield count_paths(graph, "start", {"start"})
    yield count_paths(graph, "start", {"start"}, allow_second_visit=True)


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
