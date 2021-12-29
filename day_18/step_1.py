
# python script for AdventOfCode 2021, day 18, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from copy import deepcopy
from itertools import product

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# some functions ...
def new_node(value=None, left= None, right=None):
    return {"value" : value, 
            "left"  : left,
            "right" : right, }

def parse_snailfish_str(s):
    # first check for a single digit
    if len(s) == 1:
        if not s.isdigit():
            raise ValueError("Invalid snailfish_str (len=1, no digit)")
        return new_node(value = int(s))        
    # second check for brackets and left right
    if s[0] != "[" or s[-1] != "]":
        raise ValueError("Invalid snailfish_str (bracket error)")
    bracket_depth = 0
    for i,c in enumerate(s):
        if c == "[" : bracket_depth += 1
        if c == "]" : bracket_depth -= 1
        if c == "," and bracket_depth == 1:
            return new_node( left  = parse_snailfish_str(s[1:i]), 
                             right = parse_snailfish_str(s[i+1:-1]) )
    raise ValueError("Invalid snailfish_str (syntax error)", s)

def snailfish_str(sf_node):
    if sf_node["value"] != None:
        return str(sf_node["value"])
    else:
        return "[" + snailfish_str(sf_node["left"]) + "," + snailfish_str(sf_node["right"]) + "]"

def print_snailfish(sf):
    inorder = inorder_list(sf)
    for item in inorder:
        prefix = "    " * item["depth"]
        print(prefix, item["node"]["value"] if item["regular"] else "<")

def add_snailfish(sf1,sf2):
    # Quote from the AoC site:
    #
    #  To add two snailfish numbers, form a pair from the left and right parameters 
    #  of the addition operator. 
    #  There's only one problem: snailfish numbers must always be reduced    
    return reduce(new_node(left=sf1, right=sf2))

def inorder_list(node, depth=0):
    retval = []
    if node == None:
        return []
    this_list  = [ { "node"    : node,
                     "depth"   : depth,
                     "regular" : node["value"] != None } ]  
    left_list  = inorder_list(node["left"], depth+1)
    right_list = inorder_list(node["right"], depth+1)
    return left_list + this_list + right_list

def explode(sf):
    # check if we need to 'explode' something, if so
    #   - explode the first occurence
    #   - return True
    # else:
    #   - return False
    # note: sf is changed 'inplace'
    inorder = inorder_list(sf)
    max_depth = max([item["depth"] for item in inorder])
    if max_depth > 5:
        raise ValueError("Invalid snailfish, depth > 5")
    for i, item in enumerate(inorder):
        if item["depth"] == 4 and not item["regular"]:
            left_value = item["node"]["left"]["value"]
            right_value = item["node"]["right"]["value"]
            left_items = inorder[:i-1] # -1 skip 'left_value'
            left_items.reverse()  # 
            for li in left_items:
                if li["regular"]:
                    li["node"]["value"] += left_value
                    break
            right_items = inorder[i+2:] # +2 skip 'right_value'
            for ri in right_items:
                if ri["regular"]:
                    ri["node"]["value"] += right_value
                    break
            # change item under consideration to regular node with value 0
            item["node"]["value"] = 0
            item["node"]["left"] = None
            item["node"]["right"] = None
            return True
    return False

def split(sf):
    # check if we need to 'split' something, if so
    #   - split the first occurence
    #   - return True
    # else:
    #   - return False
    # note: sf is changed 'inplace'
    inorder = inorder_list(sf)
    for item in inorder:
        if item["regular"] and item["node"]["value"] >= 10:
            # split this item
            value = item["node"]["value"]
            if value % 2 == 0:
                value_left  = value // 2
                value_right = value // 2 
            else:
                value_left  = value // 2
                value_right = value // 2 + 1 
            # change the node
            item["node"]["value"]  = None
            item["node"]["left"]   = new_node(value=value_left)
            item["node"]["right"]  = new_node(value=value_right)
            return True
    return False

def reduce(sf):
    # explode and split a snailfish untill we are done, quote from the AoC site:
    #
    #   To reduce a snailfish number, you must repeatedly do the first action
    #   in this list that applies to the snailfish number:
    #   - If any pair is nested inside four pairs, the leftmost such pair explodes.
    #   - If any regular number is 10 or greater, the leftmost such regular number splits.
    #   Once no action in the above list applies, the snailfish number is reduced.
    #   
    #   During reduction, at most one action applies, after which the process returns to 
    #   the top of the list of actions. For example, if split produces a pair that meets 
    #   the explode criteria, that pair explodes before other splits occur.
    while True:
        while explode(sf):
            pass
        if not split(sf):
            break # we're done
    return sf

def magnitude(sf_node):
    # quote from the AoC site:
    #
    #   The magnitude of a pair is 3 times the magnitude of its left element plus 2 times 
    #   the magnitude of its right element. The magnitude of a regular number is just 
    #   that number.
    if sf_node["value"] != None:
        return sf_node["value"]
    else:
        return 3 * magnitude(sf_node["left"]) + 2 * magnitude(sf_node["right"])

print("=== part 1 ===")

sf_numbers = []
for line in lines:
    sf_numbers.append(parse_snailfish_str(line.strip()))

accumulator = sf_numbers[0]
for sf in sf_numbers[1:]:
    accumulator = add_snailfish(accumulator, sf)
print("Answer ", magnitude(accumulator))

print("=== part 2 ===")

sums = []
for l1 in lines:
    for l2 in lines:
        if l2 != l1:
            sf1 = parse_snailfish_str(l1.strip())
            sf2 = parse_snailfish_str(l2.strip())
            sums.append(magnitude(add_snailfish(sf1,sf2)))
print("Answer ", max(sums))

