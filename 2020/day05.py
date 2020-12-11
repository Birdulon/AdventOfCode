import numpy as np
trans = str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})
with open('input05', 'r') as file:
  sids = np.array(sorted([int(line.strip().translate(trans), 2) for line in file.readlines()]))

print(f'Part 1: {sids[-1]}')
print(f'Part 2: {sids[:-1][(sids[1:]-sids[:-1]) > 1][0]+1}')
