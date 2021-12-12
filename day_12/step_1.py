
# python script for AdventOfCode 2021, day 12, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import pprint
pp = pprint.PrettyPrinter(indent=4)

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# store connections in a dictionary, keys   : cave names, 
#                                    values : sets of connecting cave names
connections = {}

def add_to_connections(cave_from, cave_to):
    if cave_to != 'start':     # we do not go back to start (i think)
        if cave_from in connections.keys():
            connections[cave_from].add(cave_to)
        else:
            connections[cave_from] = set([cave_to])

for line in lines:
    cave_1, cave_2 = line.strip().split("-")
    add_to_connections(cave_1, cave_2)  # forwards...
    add_to_connections(cave_2, cave_1)  # ... and backwards

if test_mode:
     pp.pprint(connections)

print("=== part 1 ===")

# we store a path in a list (of ordered visited caves)
# completed paths are stored in:
completed_paths = []

def expand_path(path):
    current_cave = path[-1]
    for next_cave in connections[current_cave]:
        next_path = path.copy()
        next_path.append(next_cave)
        if next_cave == 'end':
            # we're finished
            completed_paths.append(next_path)
        elif next_cave.islower() and next_cave in path:
            pass # we cannot go there again
        else:
            expand_path(next_path)

# we will start at... cave 'start'
expand_path(["start"])
if test_mode:
    pp.pprint(completed_paths)
print("Number of paths", len(completed_paths))


print("=== part 2 ===")

def expand_path_part_2(path):
    current_cave = path[-1]
    for next_cave in connections[current_cave]:
        next_path = path.copy()
        next_path.append(next_cave)
        if next_cave == 'end':
            # we're finished
            completed_paths.add(tuple(next_path))
        elif (   # the trickey bit, identify paths we do not have to follow...
                 (
                       next_cave == special_small_cave  
                   and path.count(next_cave) >= 2
                 ) 
                 or
                 (
                        next_cave != special_small_cave  
                    and next_cave.islower() 
                    and next_cave in path
                 )
             ):
            pass # we cannot go there again
        else:
            expand_path_part_2(next_path)

small_caves = [cave for cave in connections.keys() if cave.islower() and 
                                                      cave != 'start' and 
                                                      cave != 'end']

# for part 2 we change 'completed_paths' to a set of tuples of paths:
#  - to avoid doubles    caused by looping over small_caves
#  - to increase speed   because sets are fast & fun & tuples are immutable
completed_paths = set() 

for special_small_cave in small_caves:
    expand_path_part_2(["start"])

print("Number of paths", len(completed_paths))

