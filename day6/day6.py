from tqdm import trange

with open(file, "r") as f:
    line = f.readline()

init = [int(x) for x in line.strip().split(",")]

init = [0]

for day in trange(256):
    new = []
    for fish in init:
        if fish == 0:
            new.append(6)
            new.append(8)
        else:
            new.append(fish - 1)
    init = new

    print(len(init))

dcc = dict(Counter(init))

for day in trange(256):

    nd = defaultdict(int)

    for day, numfish in dcc.items():
        if day == 0:
            nd[6] += numfish
            nd[8] += numfish
        else:
            nd[day - 1] += numfish

    dcc = nd

print(sum(dcc.values()))
