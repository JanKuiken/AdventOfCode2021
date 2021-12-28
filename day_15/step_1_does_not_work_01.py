
# python script for AdventOfCode 2021, day 15, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = True

import numpy as np
from itertools import permutations

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

print("=== part 1 ===")

# we moeten van (row,col) = (0,0) naar (9,9) voor de testdata en naar (99,99)
# voor de echte data. Als we er vanuit dat we alleen maar naar benden en
# rechts bewegen (zoals in het voorbeeld) is het 'quite doable'
# (assumption is the m... of all f...u.., ...), oke proberen

# we hebben dan 9 (99 voor de echte data) stappen beneden nodig en hetzelfde
# aantal stappen naar rechts...

# Python's itertools.permutations is our friend again

down_steps  = 'd' * (max_row - 1)
right_steps = 'r' * (max_col - 1)
all_steps   = down_steps + right_steps

min_risk = 999999999999
for route in permutations(all_steps, len(all_steps)):
    row, col = 0,0 # start position
    risk = 0
    for direction in route:
        if direction == 'd' : row += 1
        if direction == 'r' : col += 1
        risk += data[row,col]
    if risk < min_risk:
        print(risk, route)
        min_risk = risk

print("=== part 2 ===")


