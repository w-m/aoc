import pandas as pd
import sys


def day2a(file):

    df = pd.read_csv(file, header=None, delimiter=" ", names=["direction", "units"])

    total = df.groupby("direction").sum()
    total_mult = total.loc["forward"] * (total.loc["down"] - total.loc["up"])
    return total_mult.units


def day2b(file):

    df = pd.read_csv(file, header=None, delimiter=" ", names=["direction", "units"])
    down = df["direction"] == "down"
    up = df["direction"] == "up"
    forward = df["direction"] == "forward"

    df["aim_diff"] = 0

    # down X increases your aim by X units
    df.loc[down, "aim_diff"] = df[down].units

    # up X decreases your aim by X units
    df.loc[up, "aim_diff"] = -df[up].units

    df["aim"] = df.aim_diff.cumsum()

    # forward X does two things
    # - It increases your horizontal position by X units
    df["horiz_pos_diff"] = 0
    df.loc[forward, "horiz_pos_diff"] = df[forward].units
    df["horiz_pos"] = df.horiz_pos_diff.cumsum()

    # - It increases your depth by your aim multiplied by X
    df["depth_diff"] = 0
    df.loc[forward, "depth_diff"] = df[forward].aim * df[forward].units
    df["depth"] = df.depth_diff.cumsum()

    # What do you get if you multiply your final horizontal position by your final depth?
    last_state = df.iloc[-1]

    return last_state.horiz_pos * last_state.depth


assert day2a("test_input.txt") == 150
print(f"Day 2a: {day2a('input.txt')}")

assert day2b("test_input.txt") == 900
print(f"Day 2b: {day2b('input.txt')}")
