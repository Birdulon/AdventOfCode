with open('day13-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np

codes = {
  ' ': 0,
  '-': 1,
  '|': 2,
  '+': 3,
  '/': 4,
  '\\': 5,
}
carts = {
  '>': (0, 1),
  'v': (1, 2),
  '<': (2, 1),
  '^': (3, 2),
}
directions = np.array([[1,0], [0,1], [-1,0], [0,-1]])
turns = [-1, 0, 1]

grid = np.zeros((len(data[0]), len(data)), dtype=np.int64)
minecarts = []

for y, line in enumerate(data):
  for x, char in enumerate(line):
    if char in codes:
      grid[x,y] = codes[char]
    else:
      grid[x,y] = carts[char][1]
      minecarts.append(np.array([x, y, carts[char][0], 0]))

while len(minecarts) > 1:
  minecarts = sorted(minecarts, key=lambda c: (c[1], c[0]))
  i = 0
  while i < len(minecarts):
    mc = minecarts[i]
    mc[:2] += directions[mc[2]]
    g = grid[tuple(mc[:2])]

    if g in (1, 2):
      pass
    elif g == 4:
      mc[2] = (3, 2, 1, 0)[mc[2]]
    elif g == 5:
      mc[2] = (1, 0, 3, 2)[mc[2]]
    elif g == 3:
      mc[2] = (mc[2] + turns[mc[3]]) % 4
      mc[3] = (mc[3] + 1) % 3

    for j, mc2 in enumerate(minecarts):
      if j == i:
        continue
      if np.array_equal(mc[:2], mc2[:2]):
        print(f'Crash at {mc[0]},{mc[1]}')  # First crash is Part 1
        if j > i:
          minecarts.pop(j)
          minecarts.pop(i)
          i -= 1
        else:
          minecarts.pop(i)
          minecarts.pop(j)
          i -= 2
        break

    i += 1

mc = minecarts[0]
print(f'Last cart at {mc[0]},{mc[1]} with direction {mc[2]} and next intersection turn {mc[3]}')  # Part 2
