import numpy as np

def count_xmas(grid):
    count = 0
    
    for row in grid:
        count += "".join(row).count("XMAS")
        count += "".join(row[::-1]).count("XMAS")

    return count


grid = []

with open("input.txt", "r") as f:
    for line in f:
        grid.append(list(line.strip()))

linear_grid = np.array(grid)

# diag_grid_fw = np.roll(linear_grid, range(-linear_grid.shape[0], 0), axis=0)[:, ::-1]
# diag_grid_fw = np.triu(diag_grid_fw)
# diag_grid_fw[diag_grid_fw == ""] = " "

# diag_grid_bw = np.roll(linear_grid[:, ::-1], range(linear_grid.shape[0]), axis=0)
# diag_grid_bw = np.triu(diag_grid_bw)
# diag_grid_bw[diag_grid_bw == ""] = " "

# a_count = count_xmas(linear_grid) + count_xmas(linear_grid.T) + count_xmas(diag_grid_fw.T) + count_xmas(diag_grid_bw.T)

# print(a_count)

# up/down
total_count = count_xmas(linear_grid) + count_xmas(linear_grid.T)

for col in range(-linear_grid.shape[1], linear_grid.shape[1]):
    total_count += "".join(np.diagonal(linear_grid, col)).count("XMAS")
    total_count += "".join(np.diagonal(linear_grid[:, ::-1], col)).count("XMAS")

    total_count += "".join(np.diagonal(linear_grid, col))[::-1].count("XMAS")
    total_count += "".join(np.diagonal(linear_grid[:, ::-1], col))[::-1].count("XMAS")



print(total_count)

b_count = 0

for row in range(1, linear_grid.shape[0] - 1):
    for col in range(1, linear_grid.shape[1] - 1):
        if linear_grid[col][row] == "A":
            tl = linear_grid[col-1][row-1]
            br = linear_grid[col+1][row+1]
            if tl == "M" and br == "S" or tl == "S" and br == "M":
                tr = linear_grid[col+1][row-1]
                bl = linear_grid[col-1][row+1]
                if tr == "M" and bl == "S" or tr == "S" and bl == "M":
                    b_count += 1
print(b_count)


# # grid = []

# # with open("test_input.txt", "r") as f:
# #     for line in f:
# #         grid.append(list(line.strip()))

# # linear_grid = np.array(grid)
# # gs = linear_grid.shape

# # for row in range(gs.shape[0]):
# #     for col in range(gs.shape[1]):
# #         # right
# #         if row <= gs.shape[0] - 3:





# grid = []

# with open("input.txt", "r") as f:
#     for line in f:
#         grid.append(list(line.strip()))

# cols = len(grid[0])
# rows = len(grid)

# gridstr = "".join("".join(row) for row in grid)

# # fw ---
# total_count = gridstr.count("XMAS")

# # bw ---
# total_count += gridstr[::-1].count("XMAS")

# # down
# for i in range(rows):
#     total_count += gridstr[i::cols].count("XMAS")

# # up
# for i in range(rows):
#     total_count += gridstr[i::cols][::-1].count("XMAS")

# # diag down/right
# for i in range(rows):
#     total_count += gridstr[i::cols + 1].count("XMAS")

# # diag up/left
# for i in range(rows):
#     total_count += gridstr[i::cols + 1][::-1].count("XMAS")

# # diag down/left
# for i in range(rows):
#     total_count += gridstr[i::cols - 1].count("XMAS")

# # diag up/right
# for i in range(rows):
#     total_count += gridstr[i::cols - 1][::-1].count("XMAS")


# print(total_count)

