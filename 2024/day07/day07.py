from tqdm import tqdm


eqs = []

with open("input.txt", "r") as f:
    for line in f:
        res, inputs = line.split(":")
        res = int(res)
        inputs = [int(i) for i in inputs.strip().split(" ")]
        eqs.append((res, inputs))



def operate_a(res, curval, inputs):
    if not inputs:
        if res == curval:
            raise Exception("Solution found")

    else:
        # add
        operate_a(res, curval + inputs[0], inputs[1:])

        # mult
        operate_a(res, curval * inputs[0], inputs[1: ])

found = 0

for left, right in tqdm(eqs):
    try:
        operate_a(left, 0, right)
    except:
        found += left

print(found)



def operate_b(res, curval, inputs):
    if not inputs:
        if res == curval:
            raise Exception("Solution found")

    else:
        # add
        operate_b(res, curval + inputs[0], inputs[1:])

        # mult
        operate_b(res, curval * inputs[0], inputs[1: ])

        # concat
        operate_b(res, int(str(curval) + str(inputs[0])), inputs[1: ])


found = 0

for left, right in tqdm(eqs):
    try:
        operate_b(left, 0, right)
    except:
        found += left

print(found)
