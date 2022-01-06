
# python script for AdventOfCode 2021, day 22, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from collections import namedtuple
from itertools import product

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# voorbeeldje van enkele regels van de input:
#   on x=-49..-5,y=-3..45,z=-29..18
#   off x=18..30,y=-20..-8,z=-3..13
# hier maken we een list van met de volgende namedtuple:

Rule = namedtuple("Rule", "on xmin xmax ymin ymax zmin zmax")

rules = []
for line in lines:
    on_off_str, ranges_str = line.split(" ")
    on = (on_off_str == "on")
    x_range_str, y_range_str, z_range_str = ranges_str.split(",")
    x_range_str = x_range_str[2:]  # strip "x="
    y_range_str = y_range_str[2:]  # strip "y="
    z_range_str = z_range_str[2:]  # strip "z="
    xmin, xmax = x_range_str.split("..")  
    ymin, ymax = y_range_str.split("..")  
    zmin, zmax = z_range_str.split("..")  
    rules.append(Rule(on, int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)))

def xyz_in_rule(x,y,z,rule):
    return (     x >= rule.xmin and x <= rule.xmax
             and y >= rule.ymin and y <= rule.ymax 
             and z >= rule.zmin and z <= rule.zmax ) 

print("=== part 1 ===")

cubes_for_part_1 = set()
for x,y,z in product(range(-50, 50 + 1), repeat = 3):
    for rule in rules[:-2]:
        if rule.on:
            if xyz_in_rule(x,y,z,rule):
                cubes_for_part_1.add((x,y,z))
        else:
            if xyz_in_rule(x,y,z,rule):
                if (x,y,z) in cubes_for_part_1:
                    cubes_for_part_1.remove((x,y,z))


print("\n\nAnswer:", len(cubes_for_part_1))

print("=== part 2 ===")

