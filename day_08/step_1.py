
# python script for AdventOfCode 2021, day 8, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import pprint
pp = pprint.PrettyPrinter(indent=4)

# hmm, eerst maar eens de data inlezen en opslaan in een ....
# list(displays/entires)  [ dict{ "all_digits"     : list ["signals"],
#                                 "output_values"  : list ["signals"]  }]

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()
data = []
for line in lines:
    all_digits_str, display_values_str = line.split("|")
    data.append(
      {
        "all_digits"     : all_digits_str.split()      ,
        "display_values" : display_values_str.split()  ,
      }
    )

if test_mode:
    print("data :")
    pp.pprint(data)

print("=== part 1 ===")
    
# hmm, this might get complicated, close reading the part 1 problem 
# description helps....

number_of_1478_digits_in_output_values = 0
N_SEGMENTS_IN_DIGITS_1478 = [2,4,3,7]
for display_entry in data:
    display_values  = display_entry["display_values"]
    for value in display_values:
        if len(value) in N_SEGMENTS_IN_DIGITS_1478:
            number_of_1478_digits_in_output_values += 1
print("digits 1,4,7,8 appearences : ",number_of_1478_digits_in_output_values)


print("=== part 2 ===")

# oke, we gaan brute force-en en wat handigheidjes van python gebruiken:
#
#  - permutations, om alle 'hussels' van "abcdefg" te bepalen (zijn er 7! = 5040)
#  - str.translate en str.maketrans
#  - sets gebruiken voor vergelijkingen

from itertools import permutations

translation_tables = []
for p in permutations("abcdefg"):
    translation = "".join(p)  # maak weer een string van een permutatie
    translation_tables.append(str.maketrans("abcdefg", translation))

# geldige segmenten voor digits 0-9
segments = {
    "abcefg"  : "0",
    "cf"      : "1",
    "acdeg"   : "2",
    "acdfg"   : "3",
    "bcdf"    : "4",
    "abdfg"   : "5",
    "abdefg"  : "6",
    "acf"     : "7",
    "abcdefg" : "8",
    "abcdfg"  : "9",
}
# sla de geldige segments ook even op in sets voor eenvoudig testen
valid_segments_sets = [ set(k) for k in segments.keys() ]


displays_values = []
for display_entry in data:  # we have 200 entries

    # kunnen we een juiste 'vertaling' vinden voor deze entry...
    all_digits      = display_entry["all_digits"]
    display_values  = display_entry["display_values"]

    for table in translation_tables:  # we have 5040 tables...
    
        if all([set(digit.translate(table)) in valid_segments_sets for digit in all_digits]):
        
            # Joeppie, een juiste translatie tabel gevonden
            translated_display_values = []
            for value in display_values:
                value = "".join(sorted(value.translate(table)))
                translated_display_values.append(segments[value])
            displays_values.append(int("".join(translated_display_values)))


print(sum(displays_values))  # wheew, net binnen de 100 regels.....

