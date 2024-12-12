from collections import defaultdict
from itertools import permutations

antennas = defaultdict(set)

with open("input.txt", "r") as f:
    for row, line in enumerate(f):
        for col, char in enumerate(line.strip()):
            if char != ".":
                position = complex(row, col)
                antennas[char].add(position)

max_row = row
max_col = col

antinodes = set()

for frequency, ant_positions in antennas.items():
    for a, b in permutations(ant_positions, r=2):
        
        diff = b - a

        left = a - diff
        right = b + diff

        if 0 <= left.real <= max_row and 0 <= left.imag <= max_col:
            antinodes.add(left)

        if 0 <= right.real <= max_row and 0 <= right.imag <= max_col:
            antinodes.add(right)

print(len(antinodes))



antinodes = set()

for frequency, ant_positions in antennas.items():
    for a, b in permutations(ant_positions, r=2):
        
        antinodes.add(a)
        antinodes.add(b)

        diff = b - a

        left = a - diff
        while 0 <= left.real <= max_row and 0 <= left.imag <= max_col:
            antinodes.add(left)
            left -= diff

        right = b + diff
        while 0 <= right.real <= max_row and 0 <= right.imag <= max_col:
            antinodes.add(right)
            right += diff

print(len(antinodes))