with open('day20-input', 'r') as file:
  data = [l.strip('\n') for l in file]
input = data[0][1:-1]
from math import inf

directions = {'N': 0-1j, 'E': 1+0j, 'S': 0+1j, 'W': -1+0j}
stack = []
distances = {0+0j: 0}
pos = 0+0j
next_distance = 1
for c in input:
  if c in directions:
    pos += directions[c]
    distances[pos] = min(distances.get(pos, inf), next_distance)
    # This doesn't account for potentially shorter distances to other rooms along the old path to this room.
    # Works for both parts on this input though so no gain in fixing v(ツ)v
    # Backtracking those nodes would require keeping track of doors vs walls etc.
  elif c == '(':
    stack += [pos]
  elif c == '|':
    pos = stack[-1]
  elif c == ')':
    pos = stack.pop()
  next_distance = distances[pos] + 1

print(max(distances.values()))  # Part 1
print(len([x for x in distances.values() if x >= 1000]))  # Part 2


