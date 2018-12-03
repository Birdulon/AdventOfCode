with open('day6-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
lights = np.zeros((1000,1000), dtype=np.int8)

for line in data:
  tokens = line.split(' ')
  x1, y1 = [int(i) for i in tokens[-3].split(',')]
  x2, y2 = [int(i)+1 for i in tokens[-1].split(',')]  # inclusive
  if tokens[0] == 'toggle':
    lights[x1:x2, y1:y2] ^= 1
  else:  # elif tokens[0] == 'turn':
    if tokens[1] == 'on':
      lights[x1:x2, y1:y2] = 1
    else:  # Off
      lights[x1:x2, y1:y2] = 0
print(np.sum(lights))  # Part 1

lights2 = np.zeros((1000,1000), dtype=np.int32)

for line in data:
  tokens = line.split(' ')
  x1, y1 = [int(i) for i in tokens[-3].split(',')]
  x2, y2 = [int(i)+1 for i in tokens[-1].split(',')]  # inclusive
  if tokens[0] == 'toggle':
    lights2[x1:x2, y1:y2] += 2
  else:  # elif tokens[0] == 'turn':
    if tokens[1] == 'on':
      lights2[x1:x2, y1:y2] += 1
    else:  # Off
      lights2[x1:x2, y1:y2] -= 1
      np.clip(lights2[x1:x2, y1:y2], 0, None, out=lights2[x1:x2, y1:y2])
print(np.sum(lights2))  # Part 2
