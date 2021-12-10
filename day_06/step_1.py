
# python script for AdventOfCode 2021, day 6, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

# first some functions....

# we store the populations in a dict, key=counter, value=number
def empty_population():
    empty = {}
    for i in range(9):
        empty[i] = 0
    return empty

def total_population(in_pop):
    return sum(in_pop.values())

def next_population(in_pop):
    next_pop = empty_population()
    next_pop[8] = in_pop[0]              # new born's
    next_pop[7] = in_pop[8]              # 1 days olds
    next_pop[6] = in_pop[7] + in_pop[0]  # 2 days olds + resets
    next_pop[5] = in_pop[6]              # yesterday's sixes
    next_pop[4] = in_pop[5]              # etc...
    next_pop[3] = in_pop[4]              # etc...
    next_pop[2] = in_pop[3]              # etc...
    next_pop[1] = in_pop[2]              # etc...
    next_pop[0] = in_pop[1]              # etc...
    return next_pop

# read initial population
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()
initial_population = empty_population()
first_line = lines[0]
for laternfish in first_line.split(","):
    initial_population[int(laternfish)] += 1

if test_mode:
    print("Initial :", 
          initial_population, 
          ", total :", 
          total_population(initial_population))

print("=== part 1 ===")

population = initial_population.copy()
for day_no in range(1, 80+1):
    population = next_population(population)
    if test_mode and (day_no==18):
        print("After 18 Days, total", total_population(population))
print("After 80 Days, total", total_population(population))


print("=== part 2 ===")

population = initial_population.copy()
for day_no in range(1, 256+1):
    population = next_population(population)
print("After 256 Days, total", total_population(population))

