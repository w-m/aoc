
def r_strlist(filename):
    """ Reads file into list of stripped strings """

    lines = []

    with open(filename, "r") as f:
        for line in f:
            lines.append(line.strip())

    return lines


def r_grid_ints(filename):

    grid = []
    for line in r_strlist(filename):
        grid.append([int(c) for c in line])

    return grid

def r_grid_chars(filename):

    grid = []
    for line in r_strlist(filename):
        grid.append(list(line))

    return grid

