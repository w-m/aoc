import numpy as np

safe = 0

with open("input.txt", "r") as f:
    for line in f:
        seq = np.array([int(a) for a in line.split(" ")])
        steps = np.unique(np.diff(seq))
        is_safe = np.all((steps >= -3) & (steps <= -1)) | np.all((steps >= 1) & (steps <= 3))
        safe += int(is_safe)

print(safe)


safe = 0

with open("input.txt", "r") as f:
    for line in f:
        org_seq = [int(a) for a in line.split(" ")]

        seq = np.array([int(a) for a in line.split(" ")])
        steps = np.unique(np.diff(seq))
        is_safe = np.all((steps >= -3) & (steps <= -1)) | np.all((steps >= 1) & (steps <= 3))
        if is_safe:
            safe += 1
        else:
            for i in range(len(seq)):
                seq = np.array([el for idx, el in enumerate(org_seq) if idx != i])

                steps = np.unique(np.diff(seq))
                is_safe = np.all((steps >= -3) & (steps <= -1)) | np.all((steps >= 1) & (steps <= 3))
                if is_safe:
                    safe += 1
                    break

print(safe)