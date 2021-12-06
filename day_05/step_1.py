
# python script for AdventOfCode 2021, day 5, see: https://adventofcode.com/

# import my favorite tool for data processing...
import numpy as np

#  Test mode uses test data and prints some debug info
test_mode = False

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# convert input lines to 3D NumPy array (dims: line_no, start/end, x/y)
data = np.zeros((len(lines), 2, 2), dtype=int)
for line_no, l in enumerate(lines):
    start, end = l.split(" -> ")
    x1, y1  = start.split(",")
    x2, y2  = end.split(",")
    data[line_no, 0, 0] = x1
    data[line_no, 0, 1] = y1
    data[line_no, 1, 0] = x2
    data[line_no, 1, 1] = y2

if test_mode:
    print(data)

def add_point_to_points_dict(d, x, y):
    if (x,y) in d.keys():
        d[(x,y)] += 1
    else:
        d[(x,y)] = 1


def calculate_points(line_data):
    '''
    returns a dict with tuple(x,y) as key and occurences as value
    '''
    points = {}
    for start,end in line_data:
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]
        if (x1 == x2):
            for y in range( min(y1,y2), max(y1,y2) + 1):
                add_point_to_points_dict(points, x1, y)
        elif (y1 == y2):
            for x in range( min(x1,x2), max(x1,x2) + 1):
                add_point_to_points_dict(points, x, y1)
        else:
            # ignore non horizontal or vertical lines
            pass
    return points

def calculate_points_2(line_data):
    '''
    returns a dict with tuple(x,y) as key and occurences as value
    '''
    points = {}
    for start,end in line_data:
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]
        if (x1 == x2):
            for y in range( min(y1,y2), max(y1,y2) + 1):
                add_point_to_points_dict(points, x1, y)
        elif (y1 == y2):
            for x in range( min(x1,x2), max(x1,x2) + 1):
                add_point_to_points_dict(points, x, y1)
        elif ( abs(x2 - x1) == abs(y2 - y1) ): # diagonals
            l = abs(x2 - x1)
            dx = np.sign(x2 - x1)
            dy = np.sign(y2 - y1)
            for d in range(l+1):
                add_point_to_points_dict(points, x1 + d * dx, y1 + d * dy)
        else:
            # ignore other lines
            pass
    return points

def print_points(points_dict):
    # determine min.max,not bulletproof, but good enough for australia and AoC
    xmax = -999999
    xmin =  999999
    ymax = -999999
    ymin =  999999
    for x,y in points_dict.keys():
        if x > xmax : xmax = x;
        if x < xmin : xmin = x;
        if y > ymax : ymax = y;
        if y < ymin : ymin = y;
    for y in range(ymin, ymax+1):
        for x in range(xmin, ymax+1):
            if (x,y) in points_dict.keys():
                print(str(int(points_dict[(x,y)])), end="")
            else:
                print(".", end="")
        print()


print("=== part 1 ===")

points = calculate_points(data)
if test_mode:
    print_points(points)
print(sum([value > 1 for value in points.values()]))


print("=== part 2 ===")

points = calculate_points_2(data)
if test_mode:
    print_points(points)
print(sum([value > 1 for value in points.values()]))


