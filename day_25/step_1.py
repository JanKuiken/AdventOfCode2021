
# python script for AdventOfCode 2021, day 25, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from collections import Counter

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

max_row = len(lines)
max_col = len(lines[0].strip())

east = set()
south = set()
for row in range(max_row):
    for col in range(max_col):
        c = lines[row][col]
        if   c == ">" : east.add((row,col))
        elif c == "v" : south.add((row,col))

def print_map(east, south):
    for row in range(max_row):
        for col in range(max_col):
            c = "."
            if (row,col) in east:  c = ">"
            if (row,col) in south: c = "v"
            print(c, end="")
        print("")

def new_map(east, south):
    new_east = set()
    new_south = set()
    # eastward bound first ...
    for row,col in east:
        new_pos = (row, (col+1) % max_col)
        if new_pos in east or new_pos in south:
            # blocked, no move
            new_east.add((row,col))
        else:
            # move
            new_east.add(new_pos)
    # ... then southward bound 
    for row,col in south:
        new_pos = ((row+1) % max_row, col)
        if new_pos in new_east or new_pos in south:
            # blocked, no move
            new_south.add((row,col))
        else:
            # move
            new_south.add(new_pos)
            
    return new_east, new_south

print("=== part 1 ===")

if test_mode: 
    print("Initial state:")
    print_map(east, south)

step = 0
while(True):
    step += 1
    new_east, new_south = new_map(east, south)
    if new_east == east and new_south == south:
        # we're done
        print("\n\nAnswer :", step, "steps\n\n")
        break
    # we have to continue
    east = new_east
    south = new_south
    if test_mode: 
        print("\nAfter ", step, "steps:")
        print_map(east, south)

print("=== part 2 ===")



