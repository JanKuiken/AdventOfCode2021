
# python script for AdventOfCode 2021, day 21, see: https://adventofcode.com/

#  Test mode uses test data and prints some debug info
test_mode = False

from itertools import product
from collections import namedtuple

# no need to read file
if test_mode:
    player_one_pos = 4 - 1    # -1, internally we have a board 0-9
    player_two_pos = 8 - 1
else:
    player_one_pos = 10 - 1
    player_two_pos =  2 - 1

# hmm, dit is anders, speciale stpe_2.py file...
print("=== part 2 ===")


possible_positions = range(10)
possible_scores = range(21)
possible_rolls = range(3)
possible_turn = range(2)

State = namedtuple("State", "player_one_pos player_two_pos player_one_score player_two_score rolls whos_turn")

# player_..._pos and player_..._score are reasonable obvious.
# but what are roll and whos_turn ... ?
# whos_turn   rolls
# 0           0       start situations, it's players 1 turn, he has rolled 0 dieces                              , (pos2 changed)
# 0           1                         it's players 1 turn, he has rolled 1 diece                                 , pos1 changed
# 0           2                         it's players 1 turn, he has rolled 2 dieces                                , pos1 changed
# 1           0       players 2 turn, he has rolled 0 dieces, but also a good state to check if player 1 has won   , pos1 changed
# 1           1       players 2 turn, he has rolled 1 dieces                                                       , pos2 changed
# 1           2       players 2 turn, he has rolled 2 dieces                                                       , pos2 changed
# 0           0       players 1 turn again, but also a good state to check if player 2 has won                     , pos2 changed


# We gaan achteruit denken, vandaar de volgende functie
def previous_state(current, last_roll):

    prev_rolls            = (current.rolls - 1) % 3
    prev_whos_turn        = current.whos_turn
    prev_player_one_score = current.player_one_score
    prev_player_two_score = current.player_two_score

    if current.rolls == 0:
        # ok, things change...
        if current.whos_turn == 1:
            prev_whos_turn = 0
            prev_player_one_score   = current.player_one_score - (current.player_one_pos + 1)
        else:
            prev_whos_turn = 1
            prev_player_two_score   = current.player_two_score - (current.player_two_pos + 1)

    if (current.whos_turn, current.rolls) in [(0,0),(1,1),(1,2)]:
        prev_player_one_pos =  current.player_one_pos
        prev_player_two_pos = (current.player_two_pos - last_roll) % 10
    else:
        prev_player_one_pos = (current.player_one_pos - last_roll) % 10
        prev_player_two_pos =  current.player_two_pos
        
    return State(
            prev_player_one_pos,
            prev_player_two_pos,
            prev_player_one_score,
            prev_player_two_score,
            prev_rolls ,
            prev_whos_turn, )

def valid_normal_state(state):
    if state.rolls == 0:
        if state.player_one_score > 20 : return False
        if state.player_two_score > 20 : return False
        if state.player_one_score < 0  : return False
        if state.player_two_score < 0  : return False
    return True
    


# we gaan  memozation gebruiken , state als key, occurences (aantal univeriums in AoC terms) als value
memozation = {}

# add all possible start states and set occurences to zero
for p1_pos, p2_pos, whos_turn in product(
        possible_positions, 
        possible_positions, 
        possible_turn
    ):
        memozation[ State (
                p1_pos,
                p2_pos,
                0,
                0,
                0,
                whos_turn
            )
        ] = 0

# set the one and only start state to one occurence
# oke our start state
start_state = State(
        player_one_pos,
        player_two_pos,
        0,               # start score
        0,               # start score 
        0,               # zero rolls rolled yet
        0,               # 0, i.e. players 1 turn
    )

winning_scores = range(21,31)
losing_scores = range(0,21)
memozation[start_state] = 1

# define winning states...
winning_states_player_one = set()
# player one wins...
for p1_pos, p2_pos, p1_sco, p2_sco in product(
            possible_positions, 
            possible_positions,
            winning_scores,
            losing_scores,
        ):
    rolls     = 0  # zero rolls rolled yet, we just finished players 1 turn
    whos_turn = 1  # 1, player one has won so it would be player twos turn
    winning_states_player_one.add(State(p1_pos, p2_pos, p1_sco, p2_sco, rolls, whos_turn))

# player two wins...
winning_states_player_two = set()
for p1_pos, p2_pos, p1_sco, p2_sco in product(
            possible_positions, 
            possible_positions,
            losing_scores,
            winning_scores,
        ):
    rolls     = 0  # zero rolls rolled yet, we just finished players 1 turn
    whos_turn = 0  # 0, player two has won so it would be player ones turn
    winning_states_player_two.add(State(p1_pos, p2_pos, p1_sco, p2_sco, rolls, whos_turn))



def number_of_states_leading_to_state(current, depth=0):
    #print(current, depth)
    global memozation
    # hebben we dit al eens gedaan...
    if current in memozation.keys():
        return memozation[current]
    
    # oke, da is jammer dan maar uitrekenen
    previous_states = [previous_state(current, last_roll) for last_roll in range(1,4)]
    number_of_states = 0
    for prev_state in previous_states:
        #print (valid_normal_state(prev_state), prev_state)
        if valid_normal_state(prev_state):
            number_of_states += number_of_states_leading_to_state(prev_state, depth+1)

    # opslaan in het collectief geheugen en waarde teruggeven
    memozation[current] = number_of_states
    return number_of_states


# oke, 1e check
#eerste_winner = list(winning_states_player_one)[1234]
#print(eerste_winner)
#print(number_of_states_leading_to_state(eerste_winner))

# the real deal
universes_where_player_one_won = 0
for state in winning_states_player_one:
    universes_where_player_one_won += number_of_states_leading_to_state(state)
    
universes_where_player_two_won = 0
for state in winning_states_player_two:
    universes_where_player_two_won += number_of_states_leading_to_state(state)

print("universes_where_player_one_won", universes_where_player_one_won)
print("universes_where_player_two_won", universes_where_player_two_won)

print("\n\nAnswer :", max(universes_where_player_one_won,universes_where_player_two_won))






