
from collections import namedtuple
from copy import deepcopy

Chunk = namedtuple("Chunk", ["len", "id"])

node_list = []

with open("input.txt", "r") as f:
    disk_map = f.read().strip()

for idx, length in enumerate(disk_map):
    length = int(length)
    if idx % 2 == 0:
        node_list.append(Chunk(len=length, id=idx//2))
    else:
        node_list.append(Chunk(len=length, id=None))

def chunklist_str(chunk_list):

    output_str = ""

    for chunk_len, chunk_id in chunk_list:
        output_str += chunk_len * str("." if chunk_id is None else chunk_id)

    return output_str

# print(chunklist_str(node_list))

def checksum(chunk_list):

    ck = 0
    block_idx = 0

    for block_len, b_id in chunk_list:

        if b_id is None:
            block_idx += block_len
        else:
            # TODO remove loop
            for i in range(block_len):
                ck += block_idx * b_id
                block_idx += 1

    return ck


# single block compaction
nl = deepcopy(node_list)

while True:

    empty_end = 0

    while True:
        chunk_len, chunk_id = nl.pop()

        if chunk_id is None:
            empty_end += chunk_len
        else:
            break

    for first_space_block_idx, (first_space_len, b_id) in enumerate(nl):
        if b_id is None:
            break

    # no more empty slots
    if b_id is not None:
        nl.append(Chunk(len=chunk_len, id=chunk_id))
        if empty_end > 0:
            nl.append(Chunk(len=empty_end, id=None))
        break

    num_filled = min(chunk_len, first_space_len)
    empty_end += num_filled

    infill = [Chunk(len=num_filled, id=chunk_id)]

    if num_filled < first_space_len:
        infill.append(Chunk(len=first_space_len - num_filled, id=None))

    nl_new = nl[:first_space_block_idx] + infill + nl[first_space_block_idx + 1:]

    if num_filled < chunk_len:
        nl_new.append(Chunk(len=chunk_len - num_filled, id=chunk_id))

    if empty_end > 0:
        nl_new.append(Chunk(len=empty_end, id=None))


    # print(chunklist_str(nl_new))
    # print(checksum(nl_new))

    nl = nl_new

# print(chunklist_str(nl))
print(checksum(nl))
# # 6461289671426


bl = deepcopy(node_list)

file_lens = {file_id: chunk_len for (chunk_len, file_id) in node_list if file_id is not None}

compact_file_id = bl[-1].id

while compact_file_id >= 0:

    # print(f"{compact_file_id=}")

    for space_block_idx, (chunk_len, file_id) in enumerate(bl):

        if file_id is not None and file_id == compact_file_id:
            break

        compact_file_len = file_lens[compact_file_id]

        if file_id is None and chunk_len >= compact_file_len:
            infill = [Chunk(len=compact_file_len, id=compact_file_id)]
            if chunk_len > compact_file_len:
                infill.append(Chunk(len=chunk_len - compact_file_len, id=None))
            bl = bl[:space_block_idx] + infill + bl[space_block_idx + 1:]

            # replace moved chunk with space
            for idx, (c_len, c_id) in enumerate(bl[::-1]):
                if c_id == compact_file_id:
                    break
            bl[len(bl) - idx - 1] = Chunk(len=compact_file_len, id=None)
            break

    compact_file_id -= 1

    # print(chunklist_str(bl))

print(checksum(bl))

