import numpy as np
from itertools import cycle
from blist import blist  # Regular lists are far too slow for Part 2, as are numpy arrays.

with open('day9-input', 'r') as file:
  data = [l.strip('\n') for l in file][0].split()
players = int(data[0])
last_marble = int(data[-2])


def find_winning_score(players, last_marble):
  marbles = blist([0])
  scores = np.zeros(players, dtype=np.int64)
  current_marble = 0
  for marble, player in zip(range(1, last_marble+1), cycle(range(players))):
    if marble % 23 == 0:
      current_marble = (current_marble-7) % len(marbles)
      scores[player] += marble + marbles.pop(current_marble)
    else:
      current_marble = (current_marble+2) % len(marbles)
      marbles.insert(current_marble, marble)
  return max(scores)


print(find_winning_score(players, last_marble))  # Part 1
print(find_winning_score(players, last_marble*100))  # Part 2
