# second attempt: rewrite as linked list

# currently only first half implemented, and it's borken: always finds a space node to continue moving to after fully compact representation is already reached
# double-linked list may not be required?

from copy import deepcopy
from dataclasses import dataclass

@dataclass
class Node:
    prev: "Node" = None
    next: "Node" = None
    file_id: int = None
    length: int = 0

    def __repr__(self):
        if self.file_id is None:
            return f"Space @ {self.length}"
        else:
            return f"{self.file_id} @ {self.length}"

with open("test_input.txt", "r") as f:
    disk_map = f.read().strip()

first_node = None

prev_node = None

for idx, length in enumerate(disk_map):
    length = int(length)

    if length:

        node = None
        if idx % 2 == 0:
            node = Node(length=length, file_id=idx//2)
        else:
            node = Node(length=length, file_id=None)

        if first_node is None:
            first_node = node
            prev_node = node
        else:
            node.prev = prev_node
            prev_node.next = node
            prev_node = node


def disk_str(node):
    if not node:
        return ""

    return node.length * str("." if node.file_id is None else node.file_id) + disk_str(node.next)

def checksum(node, blk_id=0):

    if node is None:
        return 0

    if not node.length:
        raise Exception("0-length node found")

    ck_sum = 0
    for i in range(node.length):
        if node.file_id is not None:
            ck_sum += node.file_id * blk_id
        blk_id += 1

    return ck_sum + checksum(node.next, blk_id)

print(disk_str(first_node))
print(checksum(first_node))

def last_node(node):
    if node.next:
        return last_node(node.next)
    else:
        return node

def last_file_node(node):
    cur_node = last_node(node)
    while not cur_node.file_id:
        cur_node = cur_node.prev
    return cur_node



def first_space_node(node, stop_node=None):
    if node is None:
        return None

    if stop_node is not None and id(node) == id(stop_node):
        return None

    if node.file_id is None:
        return node

    return first_space_node(node.next)

def delete_node(node):
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev

def insert_node_after(after_node, to_insert):
    next = after_node.next

    to_insert.prev = after_node
    to_insert.next = next

    after_node.next = to_insert
    
    if next:
        next.prev = to_insert

def insert_node_before(before_node, to_insert):
    prev = before_node.prev
    
    to_insert.next = before_node
    to_insert.prev = prev
    
    before_node.prev = to_insert

    if not prev:
        raise Exception("Would add node before first node, invalidating root node")

    prev.next = to_insert


def fill_space(space_node, length, file_id):
    if space_node.file_id is not None:
        raise Exception("Trying to fill a non-space node")

    if space_node.length < length:
        raise Exception("Space node has less space than required to fill")

    insert_node_before(space_node, Node(file_id=file_id, length=length))

    if space_node.length == length:
        delete_node(space_node)
    else:
        space_node.length -= length


def move_chunk(node, length):
    if node.file_id is None:
        raise Exception("Trying to move from space node")

    if length > node.length:
        raise Exception("Trying to move more than length of node")

    if node.next and node.next.file_id is None:
        node.next.length += length
    else:
        insert_node_after(node, Node(length=length))

    if length == node.length:
        delete_node(node)
        return 0
    else:
        node.length -= length
        return node.length


# compaction
first_node_a = deepcopy(first_node)

while True:

    cur_compact_node = last_file_node(first_node_a)

    print("mawp")

    if not cur_compact_node:
        break

    while True:

        # TODO keep last space_node around for faster execution
        space_node = first_space_node(first_node_a, stop_node=cur_compact_node)
        print(f"{space_node=}, {cur_compact_node=}")

        if space_node:
            space_to_fill = min(space_node.length, cur_compact_node.length)
            print(space_to_fill)
            fill_space(space_node, space_to_fill, cur_compact_node.file_id)
            remaining_length = move_chunk(cur_compact_node, space_to_fill)
            print(disk_str(first_node_a))

        if not remaining_length or not space_node:
            break

print(checksum(first_node_a))