
obstructions = set()
initial_position = None

with open("input.txt", "r") as f:
    for row, line in enumerate(f):
        for col, char in enumerate(line):
            match char:
                case "#":
                    obstructions.add(complex(row, col))
                case "^":
                    initial_position = complex(row, col)

max_row = row
max_col = col

# TODO rotate complex number?
turns = {-1: 0+1j,
         0+1j: 1,
         1: 0-1j,
         0-1j: -1}

def find_path(pos, obs):

    direction = -1
    visited = set()

    visited_dir = set()

    while 0 <= pos.real <= max_row and 0 <= pos.imag <= max_col:

        if (pos, direction) in visited_dir:
            raise Exception("Loop detected")

        visited.add(pos)
        visited_dir.add((pos, direction))

        while pos + direction in obs:
            direction = turns[direction]

        pos += direction

    return visited

orig_path = find_path(initial_position, obstructions)
print(len(orig_path))

orig_path.remove(initial_position)
loop_cands = orig_path

obs_count = 0
for cand in loop_cands:

    test_obs = obstructions.copy()
    test_obs.add(cand)

    try:
        find_path(initial_position, test_obs)
    except:
        obs_count += 1

print(obs_count)

