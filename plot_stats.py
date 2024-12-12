import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("aoc_stats.csv", index_col=0)
df_melted = df.reset_index().melt(id_vars='index', var_name='Year', value_name='Stars')
df_melted.rename(columns={'index': 'Day'}, inplace=True)

unique_years = sorted(df_melted['Year'].unique())
pal = sns.color_palette("rocket_r", n_colors=len(unique_years))

sns.set_theme(style="darkgrid")

# Absolute stars
plt.figure(figsize=(10,6))
sns.lineplot(data=df_melted, x="Day", y="Stars", hue="Year", hue_order=unique_years, palette=pal, marker='o')
plt.title("Absolute number of completed stars over days")
plt.tight_layout()
plt.savefig("aoc_stars_absolute.png")
plt.close()

# Relative normalization
relative_df = df.apply(lambda col: col / col.iloc[0])
rel_melted = relative_df.reset_index().melt(id_vars='index', var_name='Year', value_name='RelativeStars')
rel_melted.rename(columns={'index': 'Day'}, inplace=True)

plt.figure(figsize=(10,6))
sns.lineplot(data=rel_melted, x="Day", y="RelativeStars", hue="Year", hue_order=unique_years, palette=pal, marker='o')
plt.title("Relative number of completed stars (normalized by Day 1)")
plt.tight_layout()
plt.savefig("aoc_stars_relative.png")
plt.close()