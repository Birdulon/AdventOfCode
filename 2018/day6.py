with open('day6-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np

coords = [[int(i.rstrip(',')) for i in c.split()] for c in data]

def distance(c1, c2):
  dx = abs(c1[0]-c2[0])
  dy = abs(c1[1]-c2[1])
  return dx+dy

distances = {}
for coord in coords:
  distances[tuple(coord)] = [distance(coord, c2) for c2 in coords if c2 is not coord]

cell_coord = max(distances.items(), key=lambda x: min(x[1]))
field = np.zeros((500,500))

blacklist = set()
for c1 in [(x,y) for x in range(500) for y in range(500)]:
  distances = [distance(c1, c2) for c2 in coords]
  min_dist = min(distances)
  if distances.count(min_dist) == 1:
    cell = min(enumerate(distances), key=lambda x: x[1])[0]
    field[c1] = cell
    x, y = c1
    if x == 0 or y == 0 or x == 499 or y == 499:
      blacklist.add(cell)
a = [(field == i).sum() for i in range(len(coords)) if i not in blacklist]
print(max(a))

sumarea = 0
region = np.zeros((1000,1000))
for c1 in [(x,y) for x in range(-350, 350) for y in range(-350, 350)]:
  distances = [distance(c1, c2) for c2 in coords]
  total_dist = sum(distances)
  if total_dist < 10000:
    sumarea += 1
  region[c1[0]-350, c1[1]-350] = total_dist
print(sumarea)



# Part 2 not 46667 (-3000 to 3000)
# Not 46722 (<=10000)
# Not 556667 (-350 to 350)
# This is some bs