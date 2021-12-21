import numpy as np
from itertools import cycle

ex_start = [4,8]
start = [1,5]

# Part 1
def simulate(positions, target_score=1000):
    die = cycle(range(1,101))
    rolls = 0
    scores = np.array([0,0])
    while True:
        for player in range(2):
            move = next(die) + next(die) + next(die)
            rolls += 3
            positions[player] = (positions[player] + move) % 10
            scores[player] += positions[player]+1
            if scores[player] >= target_score:
                return [positions, scores, rolls]

positions, scores, rolls = simulate(np.array(start)-1)
print(f'Part 1: Final positions are {positions}, final scores are {scores}, game ended with {rolls} rolls. Answer is thus {min(scores)*rolls}')

# Part 2
# Dice probabilities:
# 3 - 1 1 1 (1) - 1/27
# 4 - 1 1 2 and permutations (3) - 3/27
# 5 - 1 1 3 (3), 1 2 2 (3) - 6/27
# 6 - 2 2 2 (1), 1 2 3 (6) - 7/27
# 7 - 3 3 1, 3 2 2 and ps - 6/27
# 8 - 3 3 2 and permutations (3) - 3/27
# 9 - 3 3 3 (1) - 1/27

# So our probability curve is:
#   3 4 5 6 7 8 9
#   . . . . . . .
#     . . . . .
#     . . . . .
#       . . .
#       . . .
#       . . .
#         .
dirac_rolls = {3:1, 9:1, 4:3, 8:3, 5:6, 7:6, 6:7}

# A naive assumption is that score per turn is uniformly distributed in [1,10] and thus the expected score per turn is 5.5
# This may not be true because of the moves but if we move an average of 6 per turn we'll cycle through the possibilities quickly
# Therefore for a target score of 21 we can expect games to last around 4 turns
# This means we might actually be able to record all possible moves to reach the target score from a given starting position!
# The dice rolls are independent events so we can completely ignore switching players for now,
#   and we can determine all of the winning roll sequences for each player individually,
#   and their number of universes (possibility weightings)
#   then we can match up those sequences in PvP with the first turn advantage to player 1 and determine probabilities from that!

# Our worst case would be something like 1,2,3,4... but this is impossible as our lowest move is 3 and our highest is 9
# We could instead get something like 4,3,2,1,4,3,2,1,4 which would take 9 moves, and is probably our worst case
# Our best cases would be 9,8,7 and all of the similar sequences to win in 3 moves
# Therefore, our move sequences are bounded to be within [3,9] moves for this ruleset

def simulate_moves_to_win(starting_position=0, score=0, moves=0, target=21, universes=1):  # 0 index for my sanity
    moves += 1
    akashic_record = {}
    for roll, subuniverses in dirac_rolls.items():
        new_pos = (starting_position + roll) % 10
        new_score = score + new_pos + 1
        if new_score >= target:  # Winning sequence
            akashic_record[(moves, True)] = akashic_record.get((moves, True),0) + universes*subuniverses
        else:  # Incomplete sequence
            akashic_record[(moves, False)] = akashic_record.get((moves, False),0) + universes*subuniverses
            subrecord = simulate_moves_to_win(new_pos, new_score, moves, target, universes*subuniverses)
            for k,v in subrecord.items():
                akashic_record[k] = akashic_record.get(k,0) + v
    return akashic_record

def solve_multiverse(starting_positions=[1,1]):  # 1 index to use from input
    p1_moves = simulate_moves_to_win(starting_positions[0]-1)
    p2_moves = simulate_moves_to_win(starting_positions[1]-1)
    p1_winning_universes = 0
    p2_winning_universes = 0
    for (turns,won), universes in p1_moves.items():
        if won:
            p1_winning_universes += universes * p2_moves.get((turns-1, False), 0)  # P1 moves before P2 so is always one ahead
    for (turns,won), universes in p2_moves.items():
        if won:
            p2_winning_universes += universes * p1_moves.get((turns, False), 0)  # P2 moves after P1 so must check same number of moves
    return p1_winning_universes, p2_winning_universes

p1w, p2w = solve_multiverse(start)
print(f'Part 2:  Player 1 wins in {p1w} universes, Player 2 wins in {p2w} universes. Answer is most wins: {max(p1w,p2w)}')
