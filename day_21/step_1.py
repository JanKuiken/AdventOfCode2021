
# python script for AdventOfCode 2021, day 21, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

import numpy as np

# no need to read file
if test_mode:
    player_one_pos = 4 - 1    # -1, internally we have a board 0-9
    player_two_pos = 8 - 1
else:
    player_one_pos = 10 - 1
    player_two_pos =  2 - 1


diece_value = 0
diece_rolls = 0
def diece_roll():
    global diece_value, diece_rolls
    diece_rolls += 1
    diece_value += 1
    if diece_value > 100:
        diece_value = 1
    return diece_value

player_one_score = 0
player_two_score = 0

def play():
    global player_one_pos, player_two_pos
    global player_one_score, player_two_score

    while True: #diece_rolls < 50:
        # player 1 plays
        steps             = diece_roll() + diece_roll() + diece_roll()
        player_one_pos    = (player_one_pos + steps) % 10
        player_one_score += (player_one_pos+1)
        if player_one_score >= 1000:
            print("Player one wins")
            print(player_one_score, player_two_score)
            print(diece_rolls)
            print("Result", diece_rolls * player_two_score)
            return

        # player 2 plays
        steps             = diece_roll() + diece_roll() + diece_roll()
        player_two_pos    = (player_two_pos + steps) % 10
        player_two_score += (player_two_pos+1)
        if player_two_score >= 1000:
            print("Player one wins")
            print(player_one_score, player_two_score)
            print(diece_rolls)
            print("Result", diece_rolls * player_one_score)
            return


print("=== part 1 ===")

play()

print("=== part 2 ===")







