
# python script for AdventOfCode 2021, day 7, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()
hpos = [int(s) for s in lines[0].split(",")]

# some functions
def calc_fuel(positions, target):
    fuel = 0
    for pos in positions:
        fuel += abs(pos - target)
    return fuel

def calc_fuel_for_step_2(positions, target):
    fuel = 0
    for pos in positions:
        n = abs(pos - target) 
        fuel += n * (n+1) // 2
    return fuel


# gewoon het gemiddelde lijkt me wel wat, 
# ff testen...
if test_mode:
    for target in range( min(hpos), max(hpos)+1):
        print(target, calc_fuel(hpos, target))
#  he toch niet???.. raar

# print some info...
if test_mode:
    print("horizontal positions", hpos)
    print("number of horizontal positions:", len(hpos))
    print("gemiddelde horizontal positions:", sum(hpos)/len(hpos))

print("=== part 1 ===")

# Que?, omdat mijn intuitie over het gemiddelde niet klopt maar gaan
# we maar even 'brute-forcen'....

fuels = []
for target in range( min(hpos), max(hpos)+1):
    fuels.append(calc_fuel(hpos, target))
print("min fuel :", min(fuels))

print("=== part 2 ===")

fuels = []
for target in range( min(hpos), max(hpos)+1):
    fuels.append(calc_fuel_for_step_2(hpos, target))
print("min fuel :", min(fuels))

