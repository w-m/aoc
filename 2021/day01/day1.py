import pandas as pd
import sys

file = sys.argv[1]

df = pd.read_csv(file, header=None)

print(f"Day 1a: {(df.diff() > 0).sum()[0]}")
print(f"Day 1b: {(df.rolling(3).sum().diff() > 0).sum()[0]}")
