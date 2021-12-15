
# python script for AdventOfCode 2021, day 14, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from collections import Counter

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

polymer_template = lines[0].strip()

pair_insertion_rules = {}
for line in lines:
    if " -> " in line:
        pair, insert = line.strip().split(" -> ")
        pair_insertion_rules[pair] = insert

if test_mode:
    print("polymer_template", polymer_template)
    print(pair_insertion_rules)


def apply_rules(polymer):
    new_polymer = ""
    for first, second in zip(polymer[:-1], polymer[1:]):
        pair = first + second
        if pair in pair_insertion_rules.keys():
            new_polymer += first + pair_insertion_rules[pair]
        else:
            new_polymer += first
    new_polymer += second # add last
    return new_polymer

print("=== part 1 ===")

polymer = polymer_template
for i in range(1, 10 + 1):
    polymer = apply_rules(polymer)
    print(i, len(polymer))
    if test_mode and i < 5:
        print(polymer)

# antwoord uitrekenen
cnt = Counter(polymer)
most_common  = cnt.most_common()[0][1]   # see python collections.Counter docs
least_common = cnt.most_common()[-1][1]  
print("answer", most_common, "-", least_common, "=", most_common-least_common)

print("=== part 2 ===")

# Oke, 'we have been warned', de polymeer wordt lang en zal niet meer in
# het geheugen van een redelijke PC passe, we moeten een list verzinnen....
#
# De hele polymeer string is sowieso niet boeiend, we gaan bijhouden hoeveel
# er van de verschillende pairs aanwezig zijn. 
#
# Nu alleen de administratie op orde krijgen en een nieuwe versie van de
# functie 'apply_rules' maken...


def add_pair_count(count_dict, pair, count):
    if pair in count_dict.keys():
        count_dict[pair] += count
    else:
        count_dict[pair] = count
    return count_dict

def init_polymer_pair_count(polymer):
    polymer_pair_count = {}  
    for first, second in zip(polymer[:-1], polymer[1:]):
        pair = first + second
        polymer_pair_count = add_pair_count(polymer_pair_count, pair, 1)
    return polymer_pair_count

def apply_rules_part_2(count_dict):
    new_count = {}
    for pair in count_dict.keys():
        if pair in pair_insertion_rules.keys():
            first, second  = pair
            insert         = pair_insertion_rules[pair]
            cnt            = count_dict[pair]
            new_count      = add_pair_count(new_count, first+insert,  cnt)
            new_count      = add_pair_count(new_count, insert+second, cnt)
        else:
            cnt            = count_dict[pair]
            new_count      = add_pair_count(new_count, first+second,  cnt)
    return new_count


polymer_count = init_polymer_pair_count(polymer_template)

for i in range(1, 40 + 1):
    polymer_count = apply_rules_part_2(polymer_count)
#    print(polymer_count)

def determine_char_count(count_dict):
    cnt = {}
    for (first, second), count in count_dict.items():
        if first in cnt.keys():
            cnt[first] += count
        else:
            cnt[first] = count
    # laatste erbij
    last_char = polymer_template[-1]  # deze blijft altijd hetzelfde
    cnt[last_char] += 1
    return cnt

# met test data is het antwoord 2188189693529
# het antwoord is niet 2566282754494, dat is te hoog

char_count = determine_char_count(polymer_count)
max_count  = max(char_count.values())
min_count  = min(char_count.values())
print("antwoord", max_count - min_count)


