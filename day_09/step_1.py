
# python script for AdventOfCode 2021, day 9, see: https://adventofcode.com/

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

# we gebruiken data als globale variabele (wordt btw niet meer veranderd).
# meer 'globals':
max_row, max_col = data.shape
# we gebruiken tuples(row,col) als indeces voor data, deze noemen we pos(itie)

if test_mode:
    print(data)

def find_neighbours(pos):
    row, col = pos
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

low_positions = []
for pos in product(range(max_row), range (max_col)):
    neighbours = find_neighbours(pos)
    if all([ data[neighbour] > data[pos] for neighbour in neighbours]):
        low_positions.append(pos)

risk_level = 0
for pos in low_positions:
    risk_level += data[pos] + 1
print("risk_level", risk_level)


print("=== part 2 ===")

# komen we er mee weg om de swamps te laten groeien tot we een 9 tegen komen?

# altijd leuk, een recursieve functie, let op: swamp is een lijst van
# posities, h.e.e.a. werkt allemaal omdat een list mutable is....
def extend_swamp(swamp, pos):
    swamp.append(pos)
    for neighbour in find_neighbours(pos):
        if not neighbour in swamp and data[neighbour] != 9:
           extend_swamp(swamp, neighbour)

swamp_sizes = []
for pos in low_positions:
    swamp = []
    extend_swamp(swamp, pos)
    swamp_sizes.append(len(swamp))

# en reken het antwoord uit (product van de grootste drie)
print("antwoord", np.product(sorted(swamp_sizes)[-3:]))

