
# python script for AdventOfCode 2021, day 19, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np
from numpy import pi, sin, cos
from itertools import product
import pprint
pp = pprint.PrettyPrinter(indent=4)


# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    all_scanners_data = f.read()

# store data in list of NumPy arrays
scanners = []
for one_scanner_data in all_scanners_data.split("\n\n"):
    lines = one_scanner_data.split("\n")
    scanner = []
    for line in lines:
        if "," in line:
            scanner.append([int(n) for n in line.split(",")])
    # nette NumPy array van maken, en bewaren
    scanners.append(np.array(scanner))

# maak rotatie matrices (netjes over tiepen van wikipedia, a ~ alpha, b ~ beta, g ~ gamma)
rotations = []
angles = [ i * pi  / 2 for i in range(4)]
for a,b,g in product(angles, repeat=3):
    rotations.append(np.array(
      [ 
        [ cos(a)*cos(b) , cos(a)*sin(b)*sin(g) - sin(a)*cos(g) , cos(a)*sin(b)*cos(g) + sin(a)*sin(g) ],
        [ sin(a)*cos(b) , sin(a)*sin(b)*sin(g) + cos(a)*cos(g) , sin(a)*sin(b)*cos(g) - cos(a)*sin(g) ],
        [-sin(b)        , cos(b)*sin(g)                        , cos(b)*cos(g)                        ], 
      ], dtype=int)
    )

# oops,... teveel, doublures eruit halen
rotations = np.array(rotations)
rotations = np.unique(rotations, axis=0) # yup 24... 
rotations = [r for r in rotations]       # make it a list again    

# we gaan set's gebruiken om punten-groepen te vergelijken, dat gaat sneller, zie verderop
def tuple_point(point):
    return tuple([coor for coor in point])
def set_of_tuple_points(points):
    return set([tuple_point(p) for p in points])

# Uitzoeken welke scanners overlap met elkaar hebben en welke transformatie 
# daarbij hoort

# We gaan de resultaten in opslaan in een dictionary
#  { (no_sc_A, no_sc_B) : (rot, shift) } met :
#    no_sc_A  - nummer van een scanner (A)
#    no_sc_B  - nummer van een scanner (B)
#    rot      - een van de vierentwintig rotatie matrices
#    shift    - vector
# Punten van scanner (B), kunnen worden omgezet in het coordinaten stelsel
# van scanner(A), door eerst te roteren met rot en dan te transleren met -shift
transformations = {}

for no_sc_A, sc_A in enumerate(scanners):
    set_sc_A = set_of_tuple_points(sc_A)
    for no_sc_B, sc_B in enumerate(scanners):
        if no_sc_B != no_sc_A:
            for irot, rot in enumerate(rotations):
                rot_sc_B = np.dot(sc_B, rot)

                # onderstaand werkt niet, sc_A[0] hoeft niet voor te komen in sc_B...:
                #p1 = sc_A[0]      
                #for p2 in rsc_B:

                for p1, p2 in product(sc_A, rot_sc_B):
                    shift = p2 - p1
                    shift_rot_sc_B = rot_sc_B - shift

                    # onderstaande werkt, maar te langzaam, we gaan sets gebruiken:    
                    #count = 0
                    #for test_p1, test_p2 in product(sc_A, shift_rot_sc_B):
                    #    if np.all(test_p2 == test_p1):
                    #        count += 1
                    #if count >= 12:

                    set_shift_rot_sc_B = set_of_tuple_points(shift_rot_sc_B)
                    
                    if len(set_sc_A.intersection(set_shift_rot_sc_B)) >= 12:
                        print("found overlap of scanners:", no_sc_A, no_sc_B)
                        transformations[(no_sc_A, no_sc_B)] = (rot, shift)
                        break

print("\n\n== transformations keys:")
pp.pprint(transformations.keys())


# So far so good,...
# We willen alle punten naar het coordinaten stelsel van scanner nummer 0 transformeren.
# Helaas kan dit niet altijd in 1 keer maar moet dat soms via de coordinaten stelsels van 
# andere scanners.... 
# Daarvoor moeten we weer een graph puzzeltje oplossen zoals op dag 12... (copy/past/change)

connections = {}
def add_to_connections(no_sc_A, no_sc_B):
    if no_sc_A in connections.keys():
        connections[no_sc_A].add(no_sc_B)
    else:
        connections[no_sc_A] = set([no_sc_B])

# to fill variable connections:
for no_sc_A, no_sc_B in transformations.keys():
    add_to_connections(no_sc_A, no_sc_B)

print("\n\n== connections:")
pp.pprint(connections)

# routes from scanner number 0 to other scanner numbers
path_to_scanner_0 = {0 : [0]}

def expand_path(path):
    current_sc = path[-1]
    for next_sc in connections[current_sc]:
        if next_sc in path:
            pass # we do not need to go there again
        else:
            next_path = path.copy()
            next_path.append(next_sc)
            path_to_scanner_0[next_sc] = next_path
            expand_path(next_path)

# to fill variable path_to_scanner:
expand_path([0]) 

print("\n\n== path_to_scanner_0:")
pp.pprint(path_to_scanner_0)

# Oke, we zijn er bijna, denk ik, we gaan de posities van de beacons gedetecteerd door 
# de verschillende scanners transformeren naar het coordinaten stelsel van scanner
# nummer 0.

print("=== part 1 ===")

all_beacons = set()

# punten van scanner nummer 0 gaan sowieso mee (want het coordinaten stelsel van deze
# scanner is de basis van alles).
for beacon in scanners[0]:
    all_beacons.add(tuple_point(beacon))    

for k,v in path_to_scanner_0.items():
    if k == 0:
        continue
    n = len(v)
    transformation_steps = [(v[i], v[i+1]) for i in range(n-1)]
    print("steps :", k, transformation_steps) 
    
    points = scanners[k]
    for step in reversed(transformation_steps):
        points = np.dot(points, transformations[step][0])
        points = points - transformations[step][1]

    for p in points:
        all_beacons.add(tuple_point(p))


print("\n\n== all_beacons:")
pp.pprint(all_beacons)

print("\n\n== len(all_beacons):", len(all_beacons), "( is answer for part 1)\n\n")

print("=== part 2 ===")

# Beetje hetzelfde truukje als voor deel 1, we vervangen de beacon punten van
# elke scanner door de oorsprong (punt (0,0,0))
# Manhattan distance van alle oorsprongen en het maximum daarvan is 'n eitje

all_origions = []
all_origions.append(np.array([0,0,0]))   #  for scanner number 0

for k,v in path_to_scanner_0.items():
    if k == 0:
        continue
    n = len(v)
    transformation_steps = [(v[i], v[i+1]) for i in range(n-1)]
    
    total_shift = np.array([0,0,0])
    for step in reversed(transformation_steps):
        total_shift += transformations[step][1]

    point = np.array([0,0,0])
    for step in reversed(transformation_steps):
        point = np.dot(point, transformations[step][0])
        point = point - transformations[step][1]

    all_origions.append(point)

manhattan_distances = []
for p1,p2 in product(all_origions, repeat=2):
    manhattan_distances.append(sum([abs(coor) for coor in (p2-p1)]))

print(max(manhattan_distances))

