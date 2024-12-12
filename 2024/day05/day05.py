from functools import cmp_to_key

rules = []
updates = []

with open("input.txt", "r") as f:
    for line in f:
        if "|" in line:
            a, b = line.split("|")
            rules.append((int(a), int(b)))
        elif "," in line:
            updates.append(eval(f"[{line}]"))

def cmp(a, b):
    for rule in rules:
        if rule == (a, b):
            return -1
        elif rule == (b, a):
            return 1
    return 0

count_a = count_b = 0

for upd in updates:
    sorted_up = sorted(upd, key=cmp_to_key(cmp))
    if upd == sorted_up:
        count_a += upd[len(upd) // 2]
    else:
        count_b += sorted_up[len(upd) // 2]

print(count_a)
print(count_b)