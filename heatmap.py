import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("aoc_stats.csv", index_col=0)
df.columns = df.columns.astype(int)
sns.set_theme(style="darkgrid")

# Absolute heatmap
plt.figure(figsize=(12,8))
sns.heatmap(df, cmap="rocket_r", cbar_kws={"label": "Stars Completed"}, annot=False)
plt.title("Absolute number of completed stars (Heatmap)")
plt.ylabel("Day")
plt.xlabel("Year")
plt.tight_layout()
plt.savefig("aoc_stars_absolute_heatmap_noann.png")
plt.close()

# Relative heatmap (relative to the first day's value in each year)
relative_df = df.apply(lambda col: col / col.iloc[0])

plt.figure(figsize=(12,8))
sns.heatmap(relative_df, cmap="rocket_r", cbar_kws={"label": "Relative to Day 1"}, annot=False)
plt.title("Relative number of completed stars (Heatmap)")
plt.ylabel("Day")
plt.xlabel("Year")
plt.tight_layout()
plt.savefig("aoc_stars_relative_heatmap_noann.png")
plt.close()