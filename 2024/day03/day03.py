
import re

with open("input.txt", "r") as f:
    total_sum = 0
    for line in f:
        matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', line)
        print(line)
        print(matches)
        for a, b in matches:
            total_sum += int(a) * int(b)

print(total_sum)


def parse_mul_with_state_machine(text, state):
    pattern = r"(do\(\)|don't\(\)|mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\))"
    matches = re.finditer(pattern, text)

    result = []

    for match in matches:
        token = match.group(0)
        if token == "do()":
            state = "do"
        elif token == "don't()":
            state = "don't"
        elif token.startswith("mul") and state == "do":
            # Extract numbers a and b from named groups
            a, b = int(match.group('a')), int(match.group('b'))
            result.append((a, b))

    return result, state  # Return the updated state

# Initialize state outside the loop
state = "do"  # Initial state

with open("input.txt", "r") as f:
    total_sum = 0
    for line in f:
        matches, state = parse_mul_with_state_machine(line, state)
        for a, b in matches:
            total_sum += a * b  # You don't need to convert a and b to int again

print(total_sum)