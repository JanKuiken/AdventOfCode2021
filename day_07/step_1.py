
# python script for AdventOfCode 2021, day 7, see: https://adventofcode.com/

# import my favorite tool for data processing...
import numpy as np

#  Test mode uses test data and prints some debug info
test_mode = False

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()
hpos = [int(s) for s in lines[0].split(",")]

# nwhaa, we maken er maar een NumPy array van... (is beter...)
hpos = np.array(hpos)

# some functions
def calc_fuel(positions, target):
    fuel = 0
    for pos in positions:
        fuel += abs(pos - target)
    return fuel

def calc_fuel_2(positions, target):
    fuel = 0
    for pos in positions:
        n = abs(pos - target) 
        fuel += n * (n+1) // 2
    return fuel



# gewoon het gemiddelde lijkt me wel wat, 
# ff testen...
if test_mode:
    for target in range( hpos.min(), hpos.max()+1):
        print(target, calc_fuel(hpos, target))
#  he toch niet???..

# print some info...
print("horizontal positions", hpos)
print("number of horizontal positions:", len(hpos))
print("gemiddelde horizontal positions:", hpos.mean())

print("=== part 1 ===")

# Que?, omdat mijn intuitie over het gemiddelde niet klopt maar gaan
# we maar even 'brute-forcen'....

min_fuel = 99999999999999 # that should do it...
best_target = None
for target in range( hpos.min(), hpos.max()+1):
    fuel = calc_fuel(hpos, target)
    print(target, fuel)
    if fuel <= min_fuel:
        min_fuel = fuel
        best_target = target
print("min fuel :", min_fuel)
print("best_target :", best_target)

print("=== part 2 ===")

min_fuel = 99999999999999 # that should do it...
best_target = None
for target in range( hpos.min(), hpos.max()+1):
    fuel = calc_fuel_2(hpos, target)
    print(target, fuel)
    if fuel <= min_fuel:
        min_fuel = fuel
        best_target = target
print("min fuel :", min_fuel)
print("best_target :", best_target)



