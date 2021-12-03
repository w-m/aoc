import pandas as pd


def read_df(file):
    df = pd.read_csv(file, dtype=str, header=None, names=["power"])
    df = df.power.apply(list).apply(pd.Series).astype(int)
    return df


def day3a(file):

    df = read_df(file)
    # Each bit in the gamma rate can be determined by finding the most common bit
    # in the corresponding position of all numbers in the diagnostic report
    most_freq = df.apply(pd.value_counts).idxmax()
    gamma_rate = int("".join(most_freq.astype(str)), 2)

    # epsilon rate is calculated [by] the least common bit from each position
    least_freq = (~most_freq.astype(bool)).astype(int)
    epsilon_rate = int("".join(least_freq.astype(str)), 2)

    return gamma_rate * epsilon_rate


def day3b(file):

    df = read_df(file).astype(bool)

    for col in df.columns:

        # determine the most common value (0 or 1) in the current bit position
        vc = df[col].value_counts()

        # If 0 and 1 are equally common, keep values with a 1 in the position being considered
        select = vc[True] >= vc[False]

        df = df[df[col] == select]

        if len(df) == 1:
            break

    oxy = int("".join(df.astype(int).astype(str).values[0]), 2)

    df = read_df(file).astype(bool)

    for col in df.columns:

        # determine the most common value (0 or 1) in the current bit position
        vc = df[col].value_counts()

        select = ~(vc[False] <= vc[True])

        df = df[df[col] == select]

        if len(df) == 1:
            break

    co2 = int("".join(df.astype(int).astype(str).values[0]), 2)

    # multiplying the oxygen generator rating by the CO2 scrubber rating

    return oxy * co2


assert day3a("test_input.txt") == 198
print(f"Day 3a: {day3a('input.txt')}")
assert day3a("input.txt") == 845186

assert day3b("test_input.txt") == 230
print(f"Day 3b: {day3b('input.txt')}")
