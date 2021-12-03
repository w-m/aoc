import pandas as pd


def read_df(file):
    df = pd.read_csv(file, header=None, delimiter=" ", names=["direction", "magnitude"])

    # add id as a "time" column
    df = df.rename_axis(index="time").reset_index()

    return df


def day2a(file):
    df = read_df(file)
    total = df.groupby("direction").sum()
    total_mult = total.loc["forward"] * (total.loc["down"] - total.loc["up"])
    return total_mult.magnitude


def day2b(file):
    df = read_df(file)

    # each direction becomes its own column, values either the magnitude
    # or 0 if time step has no change in this direction
    df = df.pivot_table(values="magnitude", index="time", columns="direction", fill_value=0)

    df["aim"] = df.down.cumsum() - df.up.cumsum()

    # forward X does two things
    # - It increases your horizontal position by X units
    df["horiz_pos"] = df.forward.cumsum()

    # - It increases your depth by your aim multiplied by X
    df["depth"] = (df.forward * df.aim).cumsum()

    # What do you get if you multiply your final horizontal position by your final depth?
    last_state = df.iloc[-1]

    return last_state.horiz_pos * last_state.depth


assert day2a("test_input.txt") == 150
print(f"Day 2a: {day2a('input.txt')}")

assert day2b("test_input.txt") == 900
print(f"Day 2b: {day2b('input.txt')}")
