import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("aoc_stats.csv", index_col=0)
df.columns = df.columns.astype(int)
unique_years = sorted(df.columns)
pal = sns.color_palette("rocket_r", n_colors=len(unique_years))

sns.set_theme(style="darkgrid")

# 1) Cumulative totals per year
cum_df = df.cumsum()
cum_melted = (cum_df.reset_index()
                  .melt(id_vars='index', var_name='Year', value_name='CumulativeStars')
                  .rename(columns={'index': 'Day'}))
cum_melted['Year'] = cum_melted['Year'].astype(int)

plt.figure(figsize=(10,6))
sns.lineplot(data=cum_melted, x="Day", y="CumulativeStars", hue="Year",
             hue_order=unique_years, palette=pal, marker='o')
plt.title("Cumulative number of completed stars over days")
plt.tight_layout()
plt.savefig("aoc_stars_cumulative.png")
plt.close()

# 2) Heatmap of completions
plt.figure(figsize=(12,8))
sns.heatmap(df, cmap="rocket_r", annot=True, fmt=".0f", cbar_kws={"label": "Stars Completed"})
plt.title("Heatmap of completed stars per day and year")
plt.ylabel("Day")
plt.xlabel("Year")
plt.tight_layout()
plt.savefig("aoc_stars_heatmap.png")
plt.close()

# 3) Normalized daily difference
diff_df = df.diff() / df.shift()
diff_df = diff_df.replace([np.inf, -np.inf], np.nan)
diff_df_melt = (diff_df.reset_index()
                    .melt(id_vars='index', var_name='Year', value_name='NormDiff')
                    .rename(columns={'index': 'Day'}))
diff_df_melt['Year'] = diff_df_melt['Year'].astype(int)

plt.figure(figsize=(10,6))
sns.lineplot(data=diff_df_melt, x="Day", y="NormDiff", hue="Year",
             hue_order=unique_years, palette=pal, marker='o')
plt.title("Normalized daily difference (relative to previous day)")
plt.ylabel("Normalized Difference")
plt.tight_layout()
plt.savefig("aoc_stars_normdiff.png")
plt.close()

# 4) Year-over-year growth ratio
# We'll compute this without overwriting the DataFrame each iteration
ratios = []
for y in unique_years:
    if y != unique_years[0]:  # skip the first year since it has no previous year
        prev_year = y - 1
        if prev_year in df.columns:
            ratio_col = df[y] / df[prev_year]
            ratio_df = pd.DataFrame({
                'Day': ratio_col.index,
                'Year': y,
                'YOYRatio': ratio_col.values
            })
            ratios.append(ratio_df)

if ratios:
    yoy_melt = pd.concat(ratios, ignore_index=True)
    plt.figure(figsize=(10,6))
    valid_years = [yr for yr in unique_years if yr != unique_years[0]]
    sns.lineplot(data=yoy_melt, x="Day", y="YOYRatio", hue="Year",
                 hue_order=valid_years, palette=pal[len(unique_years)-len(valid_years):], marker='o')
    plt.title("Year-over-year growth ratio (relative to previous year)")
    plt.ylabel("YOY Growth Ratio")
    plt.tight_layout()
    plt.savefig("aoc_stars_yoy_ratio.png")
    plt.close()
else:
    print("No YOY data available to plot.")