
# python script for AdventOfCode 2021, day 9, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

data = []
for line in lines:
    data.append([int(i) for i in line.strip()])

# nette NumPy array van maken
data = np.array(data)

if test_mode:
    print(data)

def find_neighbours(d,row,col):
    """
    returns a list of neighbours of row,col in 2D array d
    """
    max_row, max_col = d.shape
    neighbours = []
    if (row > 0)           : neighbours.append((row-1, col  ))
    if (row < (max_row-1)) : neighbours.append((row+1, col  ))
    if (col > 0)           : neighbours.append((row  , col-1))
    if (col < (max_col-1)) : neighbours.append((row  , col+1))
    return neighbours

def is_lowest(d, row, col, neighbours):
    value = d[row,col]
    return all([ d[neighbour] > value for neighbour in neighbours])
    
print("=== part 1 ===")

# even cryptisch doen met een bool array die gebruikt wordt voor indexing....
low_points = np.zeros_like(data, dtype=bool)
max_row, max_col = data.shape
for row in range(max_row):
    for col in range(max_col):
        value = data[row,col]
        neighbours = find_neighbours(data,row,col)
        if is_lowest(data, row, col, neighbours):
            low_points[row,col] = True

risk_level = data[low_points].sum() + low_points.sum()
print(risk_level)

print("=== part 2 ===")

# komen we er mee weg om de swamps te laten groeien tot we een 9 tegen komen?

def extend_swamp(d, swamp, row, col):
    neighbours = find_neighbours(d, row,col)
    for pos in neighbours:
        if not pos in swamp and d[pos] != 9:
           swamp.append(pos)
           extend_swamp(d, swamp, *pos)

swamp_sizes = []        
for row in range(max_row):
    for col in range(max_col):
        if low_points[row,col]:
            swamp = [(row,col)]
            extend_swamp(data, swamp, row, col)
            swamp_sizes.append(len(swamp))

print(np.product(sorted(swamp_sizes)[-3:]))



