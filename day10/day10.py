from funcy import print_durations
import pandas as pd
import numpy as np


def check_syntax(line):

    stack = []

    line = line.strip()

    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        elif char in [")", "]", "}", ">"]:
            match = stack.pop()
            if char == ")" and match != "(":
                return 3
            if char == "]" and match != "[":
                return 57
            if char == "}" and match != "{":
                return 1197
            if char == ">" and match != "<":
                return 25137

    return 0


def complete_line(lines):

    for line in lines:

        if check_syntax(line) > 0:
            continue

        stack = []

        line = line.strip()

        for char in line:
            if char in ["(", "[", "{", "<"]:
                stack.append(char)
            elif char in [")", "]", "}", ">"]:
                match = stack.pop()

        total_score = 0

        while len(stack):

            char = stack.pop()

            total_score *= 5

            if char == "(":
                total_score += 1
            elif char == "[":
                total_score += 2
            elif char == "{":
                total_score += 3
            elif char == "<":
                total_score += 4

        yield total_score


@print_durations
def day10(file):

    with open(file, "r") as f:
        lines = f.readlines()

    yield sum(check_syntax(line) for line in lines)

    line_scores = sorted(complete_line(lines))
    yield line_scores[len(line_scores) // 2]


if __name__ == "__main__":
    test_a, test_b = day10("test_input.txt")
    solution_a, solution_b = day10("input.txt")

    print(f"Day 10a test: {test_a}")
    print(f"Day 10b test: {test_b}")

    print(f"Day 10a solution: {solution_a}")
    print(f"Day 10b solution: {solution_b}")

    assert test_a == 26397
    assert test_b == 288957

    assert solution_a == 388713
    assert solution_b == 3539961434
