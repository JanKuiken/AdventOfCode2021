
# python script for AdventOfCode 2021, day 10, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from collections import deque

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()


matching_open = {
    ")" : "(",
    "]" : "[",
    "}" : "{",
    ">" : "<",
}
points = {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137,
}
open_brackets  = ["(","[","{","<"]
close_brackets = [")","]","}",">"]

print("=== part 1 ===")

total_score = 0
for line in lines:
    line = line.strip()
    stack = deque()
    for ch in line:
        if ch in open_brackets:
            stack.append(ch)
        if ch in close_brackets:
            if len(stack) == 0 or matching_open[ch] != stack[-1]:
                # corrupt
                score = points[ch]
                if test_mode:
                    print("corrupt, score:", score)
                total_score += score
                break # continue to next line
            else:
                stack.pop()
                
print("total_score", total_score)

print("=== part 2 ===")

points = {
    "(" : 1,
    "[" : 2,
    "{" : 3,
    "<" : 4,
}

line_scores = []
for line in lines:
    line = line.strip()
    stack = deque()
    for ch in line:
        if ch in open_brackets:
            stack.append(ch)
        if ch in close_brackets:
            if len(stack) == 0 or matching_open[ch] != stack[-1]:
                # corrupt
                break 
            else:
                stack.pop()
    else:  # pas op hoort bij de for-loop
        score = 0
        while(stack):
            score = 5 * score + points[stack.pop()]
        line_scores.append(score)

# calculate the middle score
line_scores.sort()
n = len(line_scores)  # we're promised n is odd
middle_index = (n-1) // 2
print("middle score", line_scores[middle_index])




            
