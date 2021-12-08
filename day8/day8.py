from funcy import print_durations
from collections import Counter, defaultdict
import numpy as np
import pandas as pd
from tqdm import trange


def read_file(file):
    with open(file, "r") as f:
        lines = f.readlines()

    patterns = []
    outputs = []

    for line in lines:
        p, o = line.strip().split(" | ")
        patterns.append([set(sp) for sp in p.split(" ")])
        outputs.append(["".join(set(op)) for op in o.split(" ")])

    return patterns, outputs


def day8b(pattern, output):

    db = np.array([list(val) for val in digits.values()]).astype(bool)
    pattern_lens = np.array([len(p) for p in pattern])

    dp = {}

    # 1: len(2)
    dp[1] = pattern[np.argmax(pattern_lens == 2)]
    # 4: len(4)
    dp[4] = pattern[np.argmax(pattern_lens == 4)]
    # 7: len(3)
    dp[7] = pattern[np.argmax(pattern_lens == 3)]
    # 8: len(7)
    dp[8] = pattern[np.argmax(pattern_lens == 7)]

    ps = pd.Series(pattern)
    ps5 = ps[ps.str.len() == 5]

    # len 5: 235
    # len 6: 069

    # 3: len(5) & has both signals from digit 1
    ps5_3 = ps5.apply(lambda x: dp[1].issubset(x))
    dp[3] = ps5[ps5_3].iloc[0]
    # 5: len(5) & has both signals from digit 4 - digit 1
    ps5_5 = ps5.apply(lambda x: (dp[4] - dp[1]).issubset(x))
    dp[5] = ps5[ps5_5].iloc[0]
    # 2: other len(5)
    dp[2] = ps5[~(ps5_3 + ps5_5)].iloc[0]

    ps6 = ps[ps.str.len() == 6]

    # 9: len(6) & 5 & 1
    ps6_9 = ps6.apply(lambda x: (dp[5] | dp[1]).issubset(x))
    dp[9] = ps6[ps6_9].iloc[0]

    # 6: len(6) & 8 - 1 + 5
    ps6_6 = ps6.apply(lambda x: ((dp[8] - dp[1]) | dp[5]).issubset(x))
    dp[6] = ps6[ps6_6].iloc[0]

    dp[0] = ps6[~(ps6_9 | ps6_6)].iloc[0]

    dpdf = pd.DataFrame((dp.keys(), dp.values())).T

    digits = []
    for o in output:
        dpdf[1].apply(lambda x: x is set(o))
        digits.append(dpdf[dpdf[1].apply(lambda x: x == set(o))][0].iloc[0])

    seq = int("".join([str(d) for d in digits]))
    return seq


@print_durations
def day8(file):

    patterns, outputs = read_file(file)
    sum_1478 = 0
    for o in outputs:
        sum_1478 += sum([1 for s in o if len(s) in [2, 3, 4, 7]])

    yield sum_1478

    sum_b = 0
    for pattern, output in zip(patterns, outputs):
        sum_b += day8b(pattern, output)

    yield sum_b


if __name__ == "__main__":
    test_a, test_b = day8("test_input.txt")
    puzzle_a, puzzle_b = day8("input.txt")

    print(f"Day 8a: {test_a}")
    print(f"Day 8b: {test_b}")

    print(f"Day 8a: {puzzle_a}")
    print(f"Day 8b: {puzzle_b}")

    assert test_a == 26
    assert test_b == 61229

    assert puzzle_a == 274
    assert puzzle_b == 1012089
