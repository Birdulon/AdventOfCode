import numpy as np
from itertools import cycle
from collections import deque

with open('day9-input', 'r') as file:
  data = [l.strip('\n') for l in file][0].split()
players = int(data[0])
last_marble = int(data[-2])


def find_winning_score(players, last_marble):
  marbles = deque([0])
  scores = np.zeros(players, dtype=np.int64)
  for marble, player in zip(range(1, last_marble+1), cycle(range(players))):
    if marble % 23 == 0:
      marbles.rotate(-7)
      scores[player] += marble + marbles.pop()
    else:
      marbles.rotate(2)
      marbles.append(marble)
  return max(scores)


print(find_winning_score(players, last_marble))  # Part 1
print(find_winning_score(players, last_marble*100))  # Part 2
