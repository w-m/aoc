import numpy as np

data = np.loadtxt("input.txt", dtype=int)
np.abs(np.diff(np.sort(data, axis=0))).sum()


counts = defaultdict(lambda: 0)
counts.update(Counter(data[:, 1]))

sum(el * counts[el] for el in data[:, 0])
