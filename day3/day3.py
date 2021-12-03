import pandas as pd
from funcy import print_durations


def read_df(file):
    df = pd.read_csv(file, dtype=str, header=None, names=["power"])

    # .apply(pd.Series) is quite slow (100 ms for input.txt)
    # df = df.power.apply(list).apply(pd.Series).astype(int)

    df = pd.DataFrame(df.power.apply(list).tolist()).astype(int)
    return df


def bool_series_to_dec(series):
    binary_string = series.astype(int).astype(str).str.cat()
    return int(binary_string, 2)


@print_durations
def day3a(file):

    df = read_df(file)
    # Each bit in the gamma rate can be determined by finding the most common bit
    # in the corresponding position of all numbers in the diagnostic report
    most_freq = df.apply(pd.value_counts).idxmax()
    gamma_rate = bool_series_to_dec(most_freq)

    # epsilon rate is calculated [by] the least common bit from each position
    least_freq = (~most_freq.astype(bool)).astype(int)
    epsilon_rate = bool_series_to_dec(least_freq)

    return gamma_rate * epsilon_rate


def life_support_rating(df, keep_bit_criterion):

    for col in df.columns:

        # determine the most common value (0 or 1) in the current bit position
        vc = df[col].value_counts()

        # keep rows where value matches the given criterium
        df = df[df[col] == keep_bit_criterion(vc)]

        # if you only have one number left, stop
        if len(df) == 1:
            break

    return bool_series_to_dec(df.iloc[0])


@print_durations
def day3b(file):

    df = read_df(file).astype(bool)

    # 1 if 1 is most common value or when 0 and 1 equally common
    oxy_val_to_keep = lambda vc: vc[True] >= vc[False]

    # 0 if 0 is most common value or when 0 and 1 equally common
    co2_val_to_keep = lambda vc: not oxy_val_to_keep(vc)

    oxy = life_support_rating(df, oxy_val_to_keep)
    co2 = life_support_rating(df, co2_val_to_keep)

    # multiplying the oxygen generator rating by the CO2 scrubber rating
    return oxy * co2


if __name__ == "__main__":

    print(f"Day 3a: {day3a('input.txt')}")
    print(f"Day 3b: {day3b('input.txt')}")

    assert day3a("test_input.txt") == 198
    assert day3b("test_input.txt") == 230

    assert day3a("input.txt") == 845186
    assert day3b("input.txt") == 4636702
