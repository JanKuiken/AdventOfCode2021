
# python script for AdventOfCode 2021, day 22, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from collections import namedtuple
from itertools import product, permutations

# read file
filename = "test_input_2.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

Line  = namedtuple("line", "min max" )
Block = namedtuple("Block", "lx ly lz" )
Rule  = namedtuple("Rule",  "on block")

rules = []
for line in lines:
    if line.startswith("#"):
        continue
    on_off_str, ranges_str = line.split(" ")
    on = (on_off_str == "on")
    x_range_str, y_range_str, z_range_str = ranges_str.split(",")
    x_range_str = x_range_str[2:]  # strip "x="
    y_range_str = y_range_str[2:]  # strip "y="
    z_range_str = z_range_str[2:]  # strip "z="
    xmin, xmax = x_range_str.split("..")
    ymin, ymax = y_range_str.split("..")
    zmin, zmax = z_range_str.split("..")
    lx = Line(int(xmin), int(xmax))
    ly = Line(int(ymin), int(ymax))
    lz = Line(int(zmin), int(zmax))
    block = Block(lx, ly, lz)
    rules.append(Rule(on, block))

print("=== part 2 ===")

# - ons belangrijkste data type is een blok met x-min,max, y-min,max, z-min,max
# - we gaan blokken opslaan van cubes die 'on' zijn.
# - rules werken we van boven naar beneden af
# - bij een 'off' rule moeten we kijken naar overlap
#   - een on kan 'opgeslokt' worden door een off-block (verdwijnt dan)
#   - bij deelse over wordt het on-blok gesplitst in deelblokken, waarbij
#        overlapblok wegvalt en de andere overblijven
# - bij een 'on' rule moeten we ook naar overlap kijken, anders krijgen we
#        bij de eind-adminstratie dubbel tellingen

def overlap_and_remainders(base, overlap):
    """
    Determine if and how a 1D line ('overlap') overlaps another ('base')
    Returns:
      - overlapped region
      - list of remaining regions of 'base'
    """
    # no overlap
    if overlap.max < base.min or overlap.min > base.max:
        return None, [base]
    # exact overlap
    if overlap.min == base.min and overlap.max == base.max:
        return base, []
    # completely inside
    if overlap.min > base.min and overlap.max < base.max:
        return overlap, [Line(base.min, overlap.min-1), Line(overlap.max+1, base.max)]
    # completely outside
    if overlap.min < base.min and overlap.max > base.max:
        return base, []
    # right exact match
    if overlap.max == base.max:
        if overlap.min < base.min:
            return base, []
        else:    # overlap.min > base.min
            return Line(overlap.min, base.max), [Line(base.min, overlap.min-1)]
    # left exact match
    if overlap.min == base.min:
        if overlap.max > base.max:
            return base, []
        else: # overlap.max < base.max
            return Line(base.min, overlap.max), [Line(overlap.max+1, base.max)]
    # left overlap
    if overlap.max < base.max:
        return Line(base.min, overlap.max), [Line(overlap.max+1, base.max)] 
    # right overlap
    if overlap.min > base.min:
        return Line(overlap.min, base.max), [Line(base.min, overlap.min-1)]    
    # did i miss a situation? :
    raise NotImplementedError("unhandled situation, notify developer")

def apply_rule(rule):
    global all_on_blocks

    # empty list (at startup.... or if every cube is turned off)
    if len(all_on_blocks) == 0 and rule.on:
        all_on_blocks.append(rule.block)
        return # we're done

    # we copy every thing to a new list and later swap them back
    new_on_blocks = []
    for on_block in all_on_blocks:
        # determine overlap in three directions
        overlap_x, remainders_x = overlap_and_remainders(on_block.lx, rule.block.lx)
        overlap_y, remainders_y = overlap_and_remainders(on_block.ly, rule.block.ly)
        overlap_z, remainders_z = overlap_and_remainders(on_block.lz, rule.block.lz)
        # check if there is overlap in all directions
        if overlap_x and overlap_y and overlap_z:
            # first add all sectioned blocks 
            # (make a list for overlaps so that we can add it to remainders)
            for lx,ly,lz in product( [overlap_x] +  remainders_x,
                                     [overlap_y] +  remainders_y,
                                     [overlap_z] +  remainders_z,  ) :
                new_on_blocks.append(Block(lx, ly, lz))
            # then remove overlapped block again
            new_on_blocks.remove(Block(overlap_x, overlap_y, overlap_z))
        else:
            new_on_blocks.append(on_block)
            
    # if we had an on rule we have to add the block of the rule
    if rule.on:
        new_on_blocks.append(rule.block)

    # copy new blocks into our global variable
    all_on_blocks = new_on_blocks

def number_of_on_cubes_inside_block(block):
    return   (1 +  block.lx.max - block.lx.min)   \
           * (1 +  block.ly.max - block.ly.min)   \
           * (1 +  block.lz.max - block.lz.min)

# initialize our memory
all_on_blocks = []

for no, rule in enumerate(rules):
    print(no, len(all_on_blocks), rule)   
    apply_rule(rule)

print("\n\nAnswer", sum([number_of_on_cubes_inside_block(b) for b in all_on_blocks]))

