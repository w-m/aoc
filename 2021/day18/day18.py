from __future__ import annotations
from dataclasses import dataclass
from os import replace
import pandas as pd
from itertools import combinations

@dataclass
class TreeNode:
    left: TreeNode
    right: TreeNode
    value: int
    depth: int
    parent: TreeNode

    def tolist(self):
        lst = []
        if self.left:
            if self.left.value != -1:
                lst.append(self.left.value)
            else:
                lst.append(self.left.tolist())
        if self.right:
            if self.right.value != -1:
                lst.append(self.right.value)
            else:
                lst.append(self.right.tolist())
        return lst
    
    def tonodelist(self):
        lst = []
        if self.left:
            if self.left.value != -1:
                lst.append(self.left)
            else:
                lst.append(self.left.tonodelist())
        if self.right:
            if self.right.value != -1:
                lst.append(self.right)
            else:
                lst.append(self.right.tonodelist())
        return lst
    
    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.left == other.left and self.right == other.right and self.value == other.value



def build_tree(number, depth=0, parent=None):
    node = TreeNode(None, None, -1, depth, parent)
    left, right = number
    if type(left) == list:
        node.left = build_tree(left, depth + 1, node)
    else:
        node.left = TreeNode(left=None, right=None, value=left, depth=depth + 1, parent=node)
    if type(right) == list:
        node.right = build_tree(right, depth+1,node)
    else:
        node.right = TreeNode(left=None, right=None, value=right, depth=depth + 1, parent=node)

    return node


def magnitude(number):
    left, right = number
    mag = 0
    if type(left) == list:
        mag += 3 * magnitude(left)
    else:
        mag += 3 * left

    if type(right) == list:
        mag += 2 * magnitude(right)
    else:
        mag += 2 * right

    return mag
    
def add(a, b):
    return [a, b]

def find_left(from_node):
    cur_node = from_node
    visited = set([cur_node])
    while True:
        # go up and first possible left that isn't on the parent path
        if parent := cur_node.parent:
            cur_node = parent
            visited.add(cur_node)
        else:
            return None
        
        # first possible left
        if cur_node.left and cur_node.left not in visited:
            cur_node = cur_node.left
            break

    while True:

        if cur_node.value != -1:
            return cur_node
        else:
            cur_node = cur_node.right

        # if cur_node.right.value == -1:
        #     cur_node = cur_node.right
        #     continue
        # else: # cur_node.value != -1:
        #     return cur_node

    return None

def find_right(from_node):
    cur_node = from_node
    visited = set([cur_node])
    while True:
        # go up and first possible right
        if parent := cur_node.parent:
            cur_node = parent
            visited.add(cur_node)
        else:
            return None
        
        # first possible right
        if cur_node.right and cur_node.right not in visited:
            cur_node = cur_node.right
            break

    while True:

        if cur_node.value != -1:
            return cur_node
        else:
            cur_node = cur_node.left

        # if cur_node.left.value == -1:
        #     cur_node = cur_node.left
        #     continue
        # else: # cur_node.value != -1:
        #     return cur_node

    return None



def node_iterator(root_node):
    return pd.core.common.flatten(root_node.tonodelist())


def explode(explosion_node):
    # add first value to leftmost value or drop
    if found_left := find_left(explosion_node):
        assert found_left.value != -1
        assert explosion_node.left.value != -1
        found_left.value += explosion_node.left.value
    # add right value to right value or drop
    if found_right := find_right(explosion_node):
        assert found_right.value != -1
        assert explosion_node.right.value != -1
        found_right.value += explosion_node.right.value
    
    # replace explosion_node with value 0
    # assert explosion_node.parent.left == explosion_node
    replace_node = TreeNode(None, None, 0, explosion_node.depth, explosion_node.parent)

    if explosion_node == explosion_node.parent.left:
        explosion_node.parent.left = replace_node
    else:
        explosion_node.parent.right = replace_node

def split(node):
    # replace with pair
    # left: half round down, right half round up
    value = node.value
    rleft = TreeNode(None, None, value // 2, node.depth + 1, None)
    rright = TreeNode(None, None, (value + 1) // 2, node.depth + 1, None)
    replacement_node = TreeNode(rleft, rright, -1, node.depth, node.parent)
    replacement_node.left.parent = replacement_node
    replacement_node.right.parent = replacement_node

    if node.parent.left == node:
        node.parent.left = replacement_node
    else:
        node.parent.right = replacement_node


def reduce_number(number):

    root = build_tree(number)
    # print(root.tolist())

    has_reduced = True

    while has_reduced:

        has_reduced = False

        # explode
        # print(root.tolist())

        needs_explosion = None

        # find the first depth=4
        # exists?
        for node in node_iterator(root):
            if node.depth > 4 and node.value != -1:
                explode(node.parent)
                has_reduced = True
                break
        
        if has_reduced:
            continue

        # split
        # TODO first to explode OR split, or 
        #      first to explode OR first to split?
        for node in node_iterator(root):
            if node.value != -1 and node.value > 9:
                split(node)
                has_reduced = True
                break
        
        # number > 9?

    # print(f"Reduced: {root.tolist()}")
    return root.tolist()

def add_and_reduce(lines):

    number = None

    for line in lines:
        line_number = eval(line.strip())
        if not number:
            number = line_number
        else:
            number = add(number, line_number)
        
        number = reduce_number(number)
    
    return number

def day18a(lines):
    number = add_and_reduce(lines)
    return magnitude(number)

def day18b(lines):    
    numbers = [eval(line.strip()) for line in lines]

    def mradd(a,b):
        return magnitude(reduce_number(add(a, b)))

    max_magn = max(max(mradd(a,b), mradd(b,a)) for (a, b) in combinations(numbers, 2))
    return max_magn



if __name__ == "__main__":
    assert magnitude([[1,2],[[3,4],5]]) == 143
    assert magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
    assert magnitude([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445
    assert magnitude([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791
    assert magnitude([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137
    assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

    assert build_tree([[1,2],[[3,4],5]]).tolist() == [[1,2],[[3,4],5]]
    assert build_tree([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).tolist() == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    assert build_tree([[[[1,1],[2,2]],[3,3]],[4,4]]).tolist() == [[[[1,1],[2,2]],[3,3]],[4,4]]
    assert build_tree([[[[3,0],[5,3]],[4,4]],[5,5]]).tolist() == [[[[3,0],[5,3]],[4,4]],[5,5]]
    assert build_tree([[[[5,0],[7,4]],[5,5]],[6,6]]).tolist() ==  [[[[5,0],[7,4]],[5,5]],[6,6]]
    assert build_tree([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).tolist() ==  [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

    assert reduce_number([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
    assert reduce_number([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
    assert reduce_number([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
    assert reduce_number([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]

    assert reduce_number([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]


    assert add_and_reduce("[1,1]\n[2,2]\n[3,3]\n[4,4]".splitlines()) == [[[[1,1],[2,2]],[3,3]],[4,4]]
    assert add_and_reduce("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]".splitlines()) == [[[[3,0],[5,3]],[4,4]],[5,5]]
    assert add_and_reduce("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]".splitlines()) == [[[[5,0],[7,4]],[5,5]],[6,6]]

    assert reduce_number([[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]]) == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

    with open("test_input_reduce.txt", "r") as f:
        assert add_and_reduce(f.readlines()) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

    with open("test_input.txt", "r") as f:
        assert day18a(f.readlines()) == 4140

    with open("test_input.txt", "r") as f:
        assert day18b(f.readlines()) == 3993

    with open("input.txt", "r") as f:
        print(day18a(f.readlines()))


    with open("input.txt", "r") as f:
        print(day18b(f.readlines()))
