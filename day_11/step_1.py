
# python script for AdventOfCode 2021, day 11, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np
from itertools import product

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

data = []
for line in lines:
    data.append([int(i) for i in line.strip()])

# nette NumPy array van maken
data = np.array(data)
original_data = data.copy()

# we gebruiken data als globale variabele.
# meer 'globals':
max_row, max_col = data.shape
# we gebruiken tuples(row,col) als indeces voor data, deze noemen we pos(itie)

if test_mode:
    print(data)

def find_neighbours(pos):
    row, col = pos
    neighbours = []
    # horizontal and vertical
    if (row > 0)           : neighbours.append((row-1, col  ))
    if (row < (max_row-1)) : neighbours.append((row+1, col  ))
    if (col > 0)           : neighbours.append((row  , col-1))
    if (col < (max_col-1)) : neighbours.append((row  , col+1))
    # diagonals
    if (row > 0)           and (col > 0)           : neighbours.append((row-1, col-1))
    if (row < (max_row-1)) and (col > 0)           : neighbours.append((row+1, col-1))
    if (row > 0)           and (col < (max_col-1)) : neighbours.append((row-1, col+1))
    if (row < (max_row-1)) and (col < (max_col-1)) : neighbours.append((row+1, col+1))
    return neighbours

print("=== part 1 ===")

def step_for_part_1():
    global data
    # increase all by one
    data += 1
    # check for flashes, and increase neighbours untill no more flashes
    flashes = 0
    while data.max() > 9:
        for pos in product(range(max_row), range (max_col)):
            if data[pos] > 9:
                flashes += 1
                data[pos] = 0
                neighbours = find_neighbours(pos)
                for neighbour in neighbours:
                    if data[neighbour] != 0:  # skip octopuses that already have flashed
                        data[neighbour] += 1
    return flashes

total_flashes = 0
for step in range(1, 100+1):
    if test_mode:
        print("step :", step)
        print(data)
    total_flashes += step_for_part_1()
print(total_flashes)

print("=== part 2 ===")

data = original_data.copy() # start with original data, not changed by part 1

for step in range(1, 999999):
    flashes = step_for_part_1()
    if flashes == max_row * max_col:
        print("all octopuses flash at step", step)
        break  # we're done

