
# python script for AdventOfCode 2021, day 8, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import pprint
pp = pprint.PrettyPrinter(indent=4)


# 7-segment-displays, hoe zit het ook al weer...
#
# 0      abc efg      6      3
# 1        c  f       2      1   *
# 2      a cde g      5      3
# 3      a cd fg      5      3
# 4       bcd f       4      1   *
# 5      ab d fg      5      3
# 6      ab defg      6      3
# 7      a c  f       3      1   *
# 8      abcdefg      7      1   *
# 9      abcd fg      6      3

# hmm, eerst maar eens de data inlezen en opslaan in een ....
# list(displays/entires)  [ dict{ "all_digits"     : list ["signals"],
#                                 "output_values"  : list ["signals"]  }]

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

data = []
for line in lines:
    all_digits_str, output_values_str = line.split("|")
    data.append(
      {
        "all_digits"     : all_digits_str.split()      ,
        "output_values"  : output_values_str.split()  ,
      }
    )

if test_mode:
    print("data :")
    pp.pprint(data)


print("=== part 1 ===")
    
# hmm, this might get complicated, close reading the part 1 problem 
# description helps....

number_of_1478_digits_in_output_values = 0
N_SEGEMNETS_IN_DIGITS_1478 = [2,4,3,7]
for display in data:
    outputs = display["output_values"]
    for output in outputs:
        if len(output) in N_SEGEMNETS_IN_DIGITS_1478:
            number_of_1478_digits_in_output_values += 1
print("digits 1,4,7,8 appearences : ",number_of_1478_digits_in_output_values)


