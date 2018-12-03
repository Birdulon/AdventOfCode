with open('day3-input', 'r') as file:
  data = [l.strip('\n') for l in file]

import numpy as np
fabric = np.zeros((1000, 1000), dtype=np.int32)

for line in data:
  tokens = line.split(' ')
  w, h = [int(i) for i in tokens[-1].split('x')]
  x, y = [int(i) for i in tokens[-2].rstrip(':').split(',')]
  fabric[x:x+w, y:y+h] += 1

print((fabric > 1).sum())  # Part 1

for line in data:
  tokens = line.split(' ')
  w, h = [int(i) for i in tokens[-1].split('x')]
  x, y = [int(i) for i in tokens[-2].rstrip(':').split(',')]
  if fabric[x:x+w, y:y+h].sum() == w*h:
    print(tokens[0])  # Part 2
    break
