
# python script for AdventOfCode 2021, day 20, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    data = f.read()


algo_data, imag_data = data.split("\n\n")

algorithm_string = [1 if c == "#" else 0 for c in algo_data]

image = set()
for row, line in enumerate(imag_data.split("\n")):
    for col, char in enumerate(line):
        if char == "#":
            image.add((row,col))


def image_size():
    image_array = np.array(list(image))
    min_row = image_array[:,0].min()
    max_row = image_array[:,0].max()
    min_col = image_array[:,1].min()
    max_col = image_array[:,1].max()
    return min_row, max_row, min_col, max_col

def print_image():
    global min_row, max_row, min_col, max_col

    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            print("#" if (row,col) in image else ".", end="")
        print()


def check_pixel(row,col):
    global image
    global min_row, max_row, min_col, max_col, inf_toggle

    if ( row >= min_row and row <= max_row and
         col >= min_col and col <= max_col     ) :
         return (row,col) in image
    else:
        if test_mode:
            return False
        else:
            return inf_toggle

def enhanced_pixel(row,col):
    index = 0
    if check_pixel(row-1,col-1) : index += 256
    if check_pixel(row-1,col  ) : index += 128
    if check_pixel(row-1,col+1) : index +=  64
    if check_pixel(row  ,col-1) : index +=  32
    if check_pixel(row  ,col  ) : index +=  16
    if check_pixel(row  ,col+1) : index +=   8
    if check_pixel(row+1,col-1) : index +=   4
    if check_pixel(row+1,col  ) : index +=   2
    if check_pixel(row+1,col+1) : index +=   1
    return algorithm_string[index]

def enhanced_image():
    global image
    global min_row, max_row, min_col, max_col, inf_toggle
    new_image = set()
    for row in range(min_row -1, max_row + 2):
        for col in range(min_col -1 , max_col + 2):
            if enhanced_pixel(row,col) == 1:
                new_image.add((row,col))
    image = new_image
    # update 'meta' stuff
    min_row -= 1
    min_col -= 1
    max_row += 1
    max_col += 1
    inf_toggle = not inf_toggle

print("=== part 1 ===")

# known area
min_row, max_row, min_col, max_col = image_size()
inf_toggle = False

print_image()
print(len(image))

enhanced_image()
print_image()
print(len(image))

enhanced_image()
print_image()
print(len(image))


print("=== part 2 ===")

for _ in range(50-2):  # -2 van part 1
    enhanced_image()

print(len(image))







