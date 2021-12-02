
# read file
with open("input.txt") as f:
    lines = f.readlines()

# starting position
hpos = 0
depth = 0

# loop over commands
for l in lines:
    direction, number = l.split()
    X = int(number)
    
    if direction == 'forward':
        hpos += X
    elif direction == 'down':
        depth += X
    elif direction == 'up':
        depth -= X
    else:
        raise ValueError("Oops unknown direction")

print("=== step one ===")
print("hpos   : ", hpos)
print("depth  : ", depth)
print("answer : ", hpos * depth)

# === part two ====

# starting position
hpos  = 0
depth = 0
aim   = 0

for l in lines:
    direction, number = l.split()
    X = int(number)
    
    if direction == 'forward':
        hpos += X
        depth += aim * X
    elif direction == 'down':
        aim += X
    elif direction == 'up':
        aim -= X
    else:
        raise ValueError("Oops unknown direction")

print("=== step two ===")
print("hpos   : ", hpos)
print("depth  : ", depth)
print("answer : ", hpos * depth)

