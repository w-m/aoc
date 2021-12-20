from funcy import print_durations
import numpy as np

# Puzzle: https://adventofcode.com/2021/day/20

# input lut: image enhancement string (512 bits)
# input img: boolean image
# 
# task:
# perform a loop of (puzzle a: 2), (puzzle b: 50) iterations of
# - look at given bool img with a 3x3 filter
# - reshape 3x3 into 9, interpret as integer value, lookup in lut
# - assume image is infinite
#
# solution:
# - 3x3 sliding window with numpy
# - initialize border around current image with value from lut

def read_img(file):
    with open(file, "r") as f:
        lookup, img = f.read().split("\n\n")
    lookup = np.array(list(lookup.replace(".", "0").replace("#", "1").replace("\n", "")), dtype=np.uint8)
    img = np.array([list(line) for line in img.replace(".", "0").replace("#", "1").splitlines()], dtype=np.uint8)
    return lookup, img

def filter_img(lookup, img, kernel, i):
    
    # grow image around border before filtering
    init_array_fn = np.zeros

    if lookup[0]:
        # infinite pixels are switching on and off
        # if they aren't turned off, there's an infinite number of 1-pixels
        assert not lookup[-1]

        # every even step has turned on all the infinite pixels
        # -> growing border has turned-on pixels
        if i % 2 == 1:    
            init_array_fn = np.ones

    grown_img = init_array_fn((img.shape[0] + 4, img.shape[1] + 4), dtype=np.uint8)
    grown_img[2:-2, 2:-2] = img
    
    # 3x3 filter
    sliding = np.lib.stride_tricks.sliding_window_view(grown_img, (3, 3))
    
    # reshape 3x3 into 9 bits
    sliding = sliding.reshape((sliding.shape[0], sliding.shape[1], -1))
    indices = np.dot(sliding, kernel)

    return lookup[indices]


def day20(file):
    lookup, img = read_img(file)
    kernel = 2 ** np.arange(8, -1, -1)

    # a: 2 iterations
    for i in range(2):
        img = filter_img(lookup, img, kernel, i)

    with np.printoptions(threshold=np.inf, linewidth=100000):
        print(np.array2string(img.astype(bool), separator="", formatter={"bool": {0: " ", 1: "█"}.get}))

    yield img.sum()

    # b: 50 iterations
    for i in range(48):
        img = filter_img(lookup, img, kernel, i)

    yield img.sum()



@print_durations
def run_expect(file, result_a, result_b):
    a, b = day20(file)
    print(f"Day 20a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 20b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":
    run_expect("test_input.txt", 35, 3351)
    run_expect("input.txt", 5301, 19492)

