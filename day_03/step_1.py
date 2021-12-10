
# python script for AdventOfCode 2021, day 3, see: https://adventofcode.com/

# import my favorite tool for data processing...
import numpy as np

#  Test mode uses test data and prints some debug info
test_mode = False

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# determine number and size of the reports
n_rows = len(lines)
n_cols = len(lines[0].strip())  # strip newline and, 
                                # assume all reports have equal length

# create a NumPy 2D array, and store the supplied data in it...
data = np.zeros((n_rows, n_cols), dtype=int)
for i, line in enumerate(lines):
    for j, ch in enumerate(line.strip()):
        data[i,j] = int(ch)

# count digits, manual check if exactly n_rows/2 does not occur...
# .. and create a binary string for the gamma value
gamma_binary_string = ""
for i in range(n_cols):
    cnt = data[:,i].sum()
    if test_mode: 
        print("column:", i, "number of ones:", cnt)
    gamma_binary_string += ["0", "1"][int(cnt > (n_rows/2))]

gamma   = int(gamma_binary_string, base=2)
epsilon = (2**n_cols - 1) - gamma            # don't ask...
power   = gamma * epsilon

print("gamma   : ", gamma)
print("epsilon : ", epsilon)
print("power   : ", power)

print("==== part 2 ====")

# small helper function
def row_to_decimal(row):
    bin_str = ""
    for value in row:
        bin_str += "1" if value == 1 else "0"
    return int(bin_str, base=2)

# oxygen
leftovers       = data.copy()
rows_left       = leftovers.shape[0]
column_to_check = 0
while (rows_left > 1):

    most_common = 1 if leftovers[:,column_to_check].sum() >= (rows_left / 2) else 0
    mask = leftovers[:,column_to_check] == most_common
    
    if test_mode:
        print(leftovers)
        print("most common for column", column_to_check, ":", most_common)
        print("mask", mask)

    leftovers       = leftovers[mask]
    rows_left       = leftovers.shape[0]
    column_to_check = (column_to_check + 1) % n_cols


oxygen = row_to_decimal(leftovers[0])
print("oxygen", oxygen)

# CO2
leftovers       = data.copy()
rows_left       = leftovers.shape[0]
column_to_check = 0
while (rows_left > 1):

    least_common = 1 if leftovers[:,column_to_check].sum() < (rows_left / 2) else 0
    mask = leftovers[:,column_to_check] == least_common
    
    if test_mode:
        print(leftovers)
        print("least common for column", column_to_check, ":", least_common)
        print("mask", mask)

    leftovers       = leftovers[mask]
    rows_left       = leftovers.shape[0]
    column_to_check = (column_to_check + 1) % n_cols


co2 = row_to_decimal(leftovers[0])
print("CO2", co2)

support_rating = oxygen * co2
print("Support rating", support_rating)


