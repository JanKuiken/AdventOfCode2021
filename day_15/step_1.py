
# python script for AdventOfCode 2021, day 15, see: https://adventofcode.com/

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
    # if (row > 0)           : neighbours.append((row-1, col  ))
    if (row < (max_row-1)) : neighbours.append((row+1, col  ))
    # if (col > 0)           : neighbours.append((row  , col-1))
    if (col < (max_col-1)) : neighbours.append((row  , col+1))
    return neighbours

def print_route(route):
    for row in range(max_row):
        for col in range(max_col):
            print('*' if (row,col) in route else ' ', end='')
            print(data[row,col], end='')
        print()
    print()

def calc_risk(route):
    return sum([data[row,col] for row,col in route[1:]])        


print("=== part 1 ===")

# we moeten van (row,col) = (0,0) naar (9,9) voor de testdata en naar (99,99)
# voor de echte data. Kijkend naar het voorbeeld en licht optimistisch
# vervolgens wij onze route met naar het laagste risk niveau bij elke stap.
# weillicht hebben we meerdere mogelijkheden met hetzelfde laagste risk level,
# vandaar dat we weer wat moeten recurvise-eren, altijd leuk....

completed_routes = []

def extend_route(route):
    last_pos = route[-1] # positie van de laatste stap
    # buren die niet al in de afgelegde weg zitten:
    possible_steps = find_neighbours(last_pos)
    possible_steps = [s for s in possible_steps if s not in route]
    if len(possible_steps) >= 1:
        min_risk = min([data[n] for n in possible_steps])
        possible_steps = [s for s in possible_steps if data[s] == min_risk]
        #print(min_risk, last_pos, possible_steps)
        for step in possible_steps:
            new_route = route.copy()
            new_route.append(step)
            if step == (max_row-1, max_col-1):
                completed_routes.append(new_route)
            else:
                extend_route(new_route)

start_route = [(0,0)]
#extend_route(start_route)

for route in completed_routes:
    print(len(route), calc_risk(route))

# oke ik kreeg mijn oplossing met extend_route niet goed, gespiekt en
# met op google gevonden https://www.youtube.com/watch?v=hig93Etxims
# (tot nog toe alleen part 1 bekeken)
# h.e.e.a. aangepast aan mijn data structuur en namen:

memozation = {}
def solve(row,col):
    if (row,col) in memozation:
        return memozation[(row,col)]
    if row < 0 or row >= max_row or col < 0 or col >= max_col:
        ans = 9999999999999999
        memozation[(row,col)] = ans
        return ans
    if row == max_row-1 and col == max_col-1:
        return data[row,col]
    ans = data[row,col] + min(solve(row+1, col  ), 
#                              solve(row-1, col  ),
#                              solve(row  , col-1),
                              solve(row  , col+1) )
    memozation[(row,col)] = ans
    return ans 

print(solve(0,0)- data[0,0])

# bizar cool:
# - recursiefiteit zoals het hoort
# - ik 'brute froce-de' te veel (en ook nog eens niet goed...)
# - note: de memozation is wel degelijk nodig voor de snelheid
# - puntje waar ik nog over denk, wat als de optimale route ook weer
#   eens 'terug' gaat in row/col waarde....

# deel 2 probeer ik weer zelf....

print("=== part 2 ===")

N = 5  # 'expand factor'
tiled_data = np.tile(data, (N,N))
for row_tile, col_tile in product(range(N), repeat=2):
    add = row_tile + col_tile
    tiled_data[row_tile * max_row : (row_tile + 1) * max_row, 
               col_tile * max_col : (col_tile + 1) * max_col  ] += add         

tiled_data = 1 + (tiled_data - 1) % 9

# terug zetten in data
data = tiled_data
max_row, max_col = data.shape

# en nog een keer   hmm,... het is niet 2835...
memozation = {}
print(solve(0,0)- data[0,0])

               




