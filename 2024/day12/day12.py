from wmaoclib.read_puzzle_input import r_grid_chars
from wmaoclib.results import run_expect

from collections import defaultdict

def merge_neighbors_single_char(elems):
    for i in range(len(elems)):
        for j in range(i+1, len(elems)):

            set_a = elems[i]
            set_b = elems[j]

            for node in set_a:
                if (node -1+0j in set_b) or (node +1+0j in set_b) or (node -1j in set_b) or (node +1j in set_b):
                    set_a.update(set_b)
                    set_b.clear()
                    return True

    return False

def merge_neighbors(cells):

    i = 0

    while True:

        has_changed = False

        for char, elems in cells.items():
            has_changed |= merge_neighbors_single_char(elems)

        if i % 1_0 == 0:
            print([len(b) for b in cells["A"]])

        i += 1

        new_cells = defaultdict(list)
        for char, elems in cells.items():
            for set_x in elems:
                if len(set_x) > 0:
                    new_cells[char].append(set_x)

        cells = new_cells


        if not has_changed:
            break


    return new_cells


def compute_borders(cells):

    total_border = 0

    for char, elems in cells.items():
        for group in elems:
            for node in group:
                num_neighbors = (node -1+0j in group) + (node +1+0j in group) + (node -1j in group) + (node +1j in group)
                total_border += (4 - num_neighbors) * len(group)

    return total_border
                


def compute_a(grid):

    cells = defaultdict(list)

    for row_id, row in enumerate(grid):
        for col_id, char in enumerate(row):
            cells[char].append(set([complex(row_id, col_id)]))


    merged = merge_neighbors(cells)

    

    return compute_borders(merged), merged

# if __name__ == "__main__":
a, a_state, b, b_state = run_expect("2024/day12/input.txt", r_grid_chars, compute_a, 1930)
