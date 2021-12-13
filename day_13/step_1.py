
# python script for AdventOfCode 2021, day 13, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=4)

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# lines with point info contain a ',', others not
points = []   # list of tuples with (x,y) integer values
for line in lines:
    if "," in line:
        x,y = line.strip().split(",")
        points.append((int(x), int(y)))
# oh no, make it a NumPy array x's are in points[:,0], y's in [:,1]:
points = np.array(points)

# store folds as a list with tuples with a 'x' or a 'y' and a value
folds = []
for line in lines:
    if "fold along" in line:
        # double split to find 'x' or 'y' and the x or y value..
        coordinate, value  = line.strip().split(" ")[-1].split("=")
        folds.append((coordinate, int(value)))

if test_mode:
    print(points)
    print(folds)

# create a 2D NumPy array with bools with the right size, fill it with points
data = np.zeros((points[:,0].max()+1, points[:,1].max()+1), dtype=bool) 
for x,y in points:
    data[x,y] = True

# cryptic function to print the data as displayed on the AoC site
def print_paper(paper):
    for row in paper.T:
        for col in row:
            print("#" if col else '.', end="")
        print()
    print("-" * 78)

def fold(paper, axis, value):
    # we doen of we dom zijn en alleen maar naar boven kunnen vouwen, als
    # we naar links moeten vouwen draaien we eerst het papier...
    paper_view = paper if axis == "y" else paper.transpose() 
    # hoe groot wordt het opgevouwen papiertje...
    n_cols, n_rows   = paper_view.shape
    n_pre_fold_rows  = value
    n_post_fold_rows = (n_rows - 1) - value
    # de vouwlijn gaat verloren, we houden het max van boven of beneden over
    n_new_rows = max(n_pre_fold_rows, n_post_fold_rows)
    # nieuw (leeg) papiertje maken....
    folded_paper = np.zeros((n_cols, n_new_rows), dtype=bool) 
    # bovenste helft invullen
    folded_paper[:, n_new_rows - n_pre_fold_rows  :                                : 1 ] += \
    paper_view  [:, 0                             : n_pre_fold_rows                : 1 ]
    # onderste helft (gespiegeld) invullen
    folded_paper[:, n_new_rows - n_post_fold_rows :                                : 1]  += \
    paper_view  [:, n_rows                        : n_rows - n_post_fold_rows - 1  :-1]
    # resultaat teruggeven (eventueel) omgedraaid
    return folded_paper if axis == "y" else folded_paper.transpose()

print("=== part 1 ===")

if test_mode:
    print_paper(data)

fold_along, value = folds[0]
data_step_1 = fold(data, fold_along, value)

if test_mode:
    print_paper(data_step_1)

print("antwoord", data_step_1.sum())

print("=== part 2 ===")

for fold_along, value in folds:
    data = fold(data, fold_along, value)

print_paper(data)


