
# python script for AdventOfCode 2021, day 12, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import pprint
pp = pprint.PrettyPrinter(indent=4)

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# store edges in a dictionary, keys: node names, values: sets of nodes names
edges = {}

def add_to_edges(node_from, node_to):
    if node_to != 'start':     # we do not go back to start (i think)
        if node_from in edges.keys():
            edges[node_from].add(node_to)
        else:
            edges[node_from] = set([node_to])

for line in lines:
    node_1, node_2 = line.strip().split("-")
    add_to_edges(node_1, node_2)
    add_to_edges(node_2, node_1)

if test_mode:
     pp.pprint(edges)

print("=== part 1 ===")

# we store a route in a list of (ordered visited nodes, completed routes
# are stored in:
completed_routes = []

def expand_route(route):
    current_node = route[-1]
    for next_node in edges[current_node]:
        next_route = route.copy()
        next_route.append(next_node)
        if next_node == 'end':
            # we're finished
            completed_routes.append(next_route)
        elif next_node.islower() and next_node in route:
            pass # we cannot go there again
        else:
            expand_route(next_route)

# we will start at... node 'start'
expand_route(["start"])
if test_mode:
    pp.pprint(completed_routes)
print("Number of routes", len(completed_routes))


print("=== part 2 ===")

completed_routes = set() # use a set of tuples for speed and to
                         # avoid doubles

def expand_route_for_part_2(route):
    current_node = route[-1]
    for next_node in edges[current_node]:
        next_route = route.copy()
        next_route.append(next_node)
        if next_node == 'end':
            # we're finished
            completed_routes.add(tuple(next_route))
        elif (
                (
                       next_node != special_small_cave  
                   and next_node.islower() 
                   and next_node in route
                 )
                 or
                 (
                        next_node == special_small_cave  
                   and  route.count(next_node) >= 2
                 ) 
             ):
            pass # we cannot go there again
        else:
            expand_route_for_part_2(next_route)

small_caves = [cave for cave in edges.keys() if cave.islower() and 
                                                cave != 'start' and 
                                                cave != 'end']
for special_small_cave in small_caves:
    expand_route_for_part_2(["start"])

print("Number of routes", len(completed_routes))

