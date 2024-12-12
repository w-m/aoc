from wmaoclib.read_puzzle_input import r_grid_ints
from wmaoclib.results import run_expect

def find_paths(grid, row_id, col_id, height, width, curval=0):

    if curval == 9:
        return [(row_id, col_id)]

    reachable = []

    candidates = [[row_id - 1, col_id],
                  [row_id + 1, col_id],
                  [row_id, col_id - 1],
                  [row_id, col_id + 1]
                 ]

    for nr, nc in candidates:
        if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == curval + 1:
            reachable += find_paths(grid, nr, nc, height, width, curval +         1)

    return reachable

def compute_a(grid):

    trail_score_a = 0
    trail_score_b = 0

    for row_id, row in enumerate(grid):
        for col_id, val in enumerate(row):

            if val == 0:
                paths = find_paths(grid, row_id=row_id, col_id=col_id, height=len(grid), width=len(grid[0]))
                trail_score_a += len(set(paths))
                trail_score_b += len(paths)

    return trail_score_a, trail_score_b


def compute_b(grid, a_state):
    return a_state, None


if __name__ == "__main__":
    run_expect("2024/day10/input.txt", r_grid_ints, compute_a, 510, compute_b, 1058)
