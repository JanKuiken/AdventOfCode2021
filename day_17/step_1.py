
# python script for AdventOfCode 2021, day 17, see: https://adventofcode.com/

# don't bother to read file, we code them manually:
test_mode = False
if test_mode:
    target_min_x =  20
    target_max_x =  30
    target_min_y = -10
    target_max_y = -5
else:
    target_min_x =  102
    target_max_x =  157
    target_min_y = -146
    target_max_y = -90

# Some sensible magic numbers (?)
MAX_STEP     = 1000
MAX_START_VY = 1000

# some functions, don't know if we use them...
def in_target_x(x):
    return x >= target_min_x and x <= target_max_x

def in_target_y(y):
    return y >= target_min_y and y <= target_max_y

def in_target(x,y):
    return in_target_x(x) and in_target_y(y)

def new_xs(x, vx):
    new_x  = x + vx
    new_vx = vx - 1 if vx > 0 else 0
    return new_x, new_vx

def new_ys(y, vy):
    new_y  = y + vy
    new_vy = vy - 1
    return new_y, new_vy


print("=== part 1 ===")

# Thoughts:
#  - we have to find start values for velocities vx and vy.
#  - we start at(0,0) and target_xs > 0 => vx must be positive.
#  - x and y problems are somewhat independent, except that x,y should end in
#    the target area during the same step.
#  - start vx must be >1 and <target_max_x+1
#  - we can stop if vx==0 and x < target_min_x
#  - we can stop if x > target_max_x

suitable_vx_step = set() 
max_suitable_x_step = 0

for start_vx in range(1, target_max_x+2):
    step = 0
    x = 0
    vx = start_vx
    while(True):
        step += 1
        x, vx = new_xs(x, vx)
        if in_target_x(x):
           suitable_vx_step.add((start_vx,step))
           max_suitable_x_step = max(max_suitable_x_step, step)
        #if vx == 0 or x > target_max_x:
        if step > MAX_STEP or x > target_max_x:
            break

highest_y = 0
suitable_vy_step = set() 
start_vy = target_min_y - 1
while True:
    start_vy += 1
    step = 0
    y = 0
    highest_y_for_this_start_vy = 0
    vy = start_vy
    while True:
        step += 1
        y, vy = new_ys(y, vy)
        highest_y_for_this_start_vy = max(highest_y_for_this_start_vy, y)
        if in_target_y(y):
            suitable_vy_step.add((start_vy,step)) 
            highest_y = max(highest_y, highest_y_for_this_start_vy) 

        if y < target_min_y or step > max_suitable_x_step:
            break
    #if y > target_max_y and step > max_suitable_x_step:
    if start_vy > MAX_START_VY:
        break

print(highest_y)

print("=== part 2 ===")

possible_vxs_for_step = {}
possible_vys_for_step = {}
possible_velocities = set()
total = 0
for step in range(1,MAX_STEP):
    possible_vxs_for_step[step] = []
    possible_vys_for_step[step] = []
    for vy,vy_step in suitable_vy_step:
        if vy_step == step:
            for vx,vx_step in suitable_vx_step:
                if vx_step == step:
                    possible_velocities.add((vx,vy))
#    for vy,vy_step in suitable_vy_step:
#        if vy_step == step:
#            print(step, vy, len(possible_vxs_for_step[step]))
#            possible_vys_for_step[step].append(vy)
#    total += ( len(possible_vxs_for_step[step]) *
#               len(possible_vys_for_step[step])    )
    
print(total)
print(len(possible_velocities))

