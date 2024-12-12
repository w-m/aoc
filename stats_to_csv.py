import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

years = range(2015, 2025)
days = range(1, 26)
data = {y: [None]*25 for y in years}

for y in years:
    time.sleep(1)  # be nice to the server
    url = f"https://adventofcode.com/{y}/stats"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.select("pre.stats a"):
        day = int(row['href'].split('/')[-1])
        if day in days:
            val = row.select_one("span.stats-both")
            data[y][day-1] = int(val.get_text(strip=True))

df = pd.DataFrame(data, index=days)
df.to_csv("aoc_stats.csv")