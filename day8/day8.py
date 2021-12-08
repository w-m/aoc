from funcy import print_durations
import pandas as pd


def day8b(row):

    pattern, outputs = row[:10], row[11:]

    # {pattern_length: [pattern, ...]}
    # e.g. {2: [{e, b}], 5: [{e, c, f, d, g}, {e, c, f, b, d}, {c, f, b, d, a}], ...}
    by_len = pattern.groupby(pattern.apply(len)).apply(list).to_dict()

    # {digit: pattern}
    digits = {
        # unique len digits
        1: by_len[2][0],
        4: by_len[4][0],
        7: by_len[3][0],
        8: by_len[7][0],
    }

    for len_5_pattern in by_len[5]:
        # 3: len(5) and has both signals from digit 1
        if digits[1].issubset(len_5_pattern):
            digits[3] = len_5_pattern
        # 5: len(5) and has both signals from (digit 4 - digit 1)
        elif (digits[4] - digits[1]).issubset(len_5_pattern):
            digits[5] = len_5_pattern
        # 2: remaining len(5) pattern
        else:
            digits[2] = len_5_pattern

    for len_6_pattern in by_len[6]:
        # 9: len(6) and has signals from (5 + 1)
        if (digits[5] | digits[1]).issubset(len_6_pattern):
            digits[9] = len_6_pattern
        # 6: len(6) and has signals frmo (8 - 1) + 5
        elif ((digits[8] - digits[1]) | digits[5]).issubset(len_6_pattern):
            digits[6] = len_6_pattern
        # 0: remaining len(6) pattern
        else:
            digits[0] = len_6_pattern

    # {pattern: digit}
    lookup = {pattern: digit for digit, pattern in digits.items()}
    output_digits = "".join([str(lookup[o]) for o in outputs])
    return int(output_digits)


@print_durations
def day8(file):

    # 10 patterns | 4 outputs
    df = pd.read_csv(file, sep=" ", header=None).applymap(frozenset)

    outputs = df.iloc[:, 11:]
    output_lens = outputs.applymap(len).melt().value.value_counts()

    # digits 1, 4, 7, and 8 each use a unique number of segments
    # num segments: 2, 3, 4, 7
    # in the output values, how many times do digits 1, 4, 7, or 8 appear?
    yield output_lens[[2, 3, 4, 7]].sum()

    yield df.apply(day8b, axis=1).sum()


if __name__ == "__main__":
    test_a, test_b = day8("test_input.txt")
    solution_a, solution_b = day8("input.txt")

    print(f"Day 8a test: {test_a}")
    print(f"Day 8b test: {test_b}")

    print(f"Day 8a solution: {solution_a}")
    print(f"Day 8b solution: {solution_b}")

    assert test_a == 26
    assert test_b == 61229

    assert solution_a == 274
    assert solution_b == 1012089
