
# python script for AdventOfCode 2021, day 4, see: https://adventofcode.com/

# import my favorite tool for data processing...
import numpy as np

#  Test mode uses test data and prints some debug info
test_mode = False

# read file
filename = "test_input.txt" if test_mode else "input.txt"
with open(filename) as f:
    lines = f.readlines()

# some sanity checks
# we have one line of calls and N cards of 5 lines seperated by 1 empty line
n_lines = len(lines)
assert (n_lines -1) % 6 == 0, "wrong number of lines"

# create a numpy int array of the first lines with calls
calls = np.asarray(lines[0].split(",")).astype(int)
n_calls = len(calls)

# create a 3D numpy array with bingo card info (card no, row , col)
n_cards = (n_lines - 1) // 6
cards = np.zeros((n_cards,5,5),dtype=int)

for board in range(n_cards):
    for row in range(5):
        str_row_values = lines[2 + 6 * board + row]
        cards[board, row] = [int(v) for v in str_row_values.split()]

if test_mode:
    print(calls)
    print(cards)

# ok write a function that checks a horziontal or vertical bingo
#                          and return bingo and calculated score
def check_bingo_card(card, calls):
    # let's use Python's sets...
    set_calls = set(calls)
    SIZE = 5

    for i in range(SIZE):
        if len(set(card[i,:]) & set_calls) == SIZE or \
           len(set(card[:,i]) & set_calls) == SIZE      :

            # BINGO ! 
            set_card    =  set(card.flatten())
            marked      = set_card & set_calls
            unmarked    = set_card ^ marked
            last_called = calls[-1]
            
            # calculate score
            sum_unmarked = np.array(list(unmarked)).sum()
            score = sum_unmarked * last_called            
            return True, score
            
    return False, -1

print("=== part 1 ===")

# oke, let's play...
break_from_two_loops = False # hmm, could this be done better...
for n in range(n_calls):
    for c in cards:
        succes, score = check_bingo_card(c, calls[:n])
        if succes:
            # we're DONE
            print("score first card with bingo :", score)
            break_from_two_loops = True

        if break_from_two_loops: break
    if break_from_two_loops: break


print("=== part 2 ===")

# determine card which has bingo has bingo very very last...
break_from_two_loops = False # hmm, could this be done better...
card_numbers_with_bingo = set()
for n in range(n_calls):
    for card_no, c in enumerate(cards):
        succes, score = check_bingo_card(c, calls[:n])
        if succes:
            card_numbers_with_bingo.add(card_no)
        if len(card_numbers_with_bingo) == n_cards:
            # we're DONE
            print("score last card with bingo :", score)
            break_from_two_loops = True

        if break_from_two_loops: break
    if break_from_two_loops: break



