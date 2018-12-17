with open('day17-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

Xmin = [int(re.findall(r'x=(\d+)', d)[0]) for d in data]
Xmax = [int(re.findall(r'x=(?:\d+\.\.)?(\d+)', d)[0]) for d in data]
Ymin = [int(re.findall(r'y=(\d+)', d)[0]) for d in data]
Ymax = [int(re.findall(r'y=(?:\d+\.\.)?(\d+)', d)[0]) for d in data]

y_min = min(Ymin)
y_max = max(Ymax)

x_min = min(Xmin) - 1
x_max = 700 - x_min

init_grid = np.zeros((x_max, y_max+1), dtype=np.int64)  # 0 = Sand, 1 = Clay, 2 = water, -1 = running water
spring = (500-x_min, 0)

for xmin, xmax, ymin, ymax in zip(Xmin, Xmax, Ymin, Ymax):
  init_grid[xmin-x_min:xmax+1-x_min, ymin:ymax+1] = 1


grid = init_grid.copy()
drop_point_blacklist = set()  # Cliff drop-offs that are guaranteed to go nowhere


def drop_water(source=spring):
  if tuple(source) in drop_point_blacklist:
    return False

  x, y = source
  surface = (grid[x, y:] > 0).argmax()
  if surface == 0:
    if (grid[x, y-1:] > 0).argmax() == 0:
      grid[x, y:] = -1
      drop_point_blacklist.add(tuple(source))
    return False
  surface_y = surface + y
  grid[x, y:surface_y] = -1

  # Find walls left and right
  wall_left = (grid[x:0:-1, surface_y-1] > 0).argmax()
  wall_right = (grid[x:, surface_y-1] > 0).argmax()
  if wall_left:
    left_x = x - wall_left + 1
    cliff = (grid[x:left_x-1:-1, surface_y] <= 0).argmax()
    if cliff:
      wall_left = False
  if wall_right:
    right_x = x + wall_right #- 1
    cliff = (grid[x:right_x, surface_y] <= 0).argmax()
    if cliff:
      wall_right = False

  if wall_right and wall_left:
    # Fill level of basin
    grid[left_x:right_x, surface_y-1] = 2
    return True

  cliffs = set()
  if not wall_left:
    cliff = int((grid[x:0:-1, surface_y] <= 0).argmax())
    grid[x-cliff:x, surface_y-1] = -1
    if wall_right:
      grid[x:right_x, surface_y - 1] = -1
    if cliff:
      cliffs.add((x - cliff, surface_y))
  if not wall_right:
    cliff = int((grid[x:, surface_y] <= 0).argmax())
    grid[x:x+cliff+1, surface_y-1] = -1
    if wall_left:
      grid[left_x:x, surface_y-1] = -1
    if cliff:
      cliffs.add((x + cliff, surface_y))

  if cliffs and len([c for c in cliffs if tuple(c) in drop_point_blacklist]) == len(cliffs):  # We go to 1 or 2 cliffs, all of which are dead-ends. We are a dead end, stop looking at us.
    drop_point_blacklist.add(tuple(source))
    return False

  succeeded = False
  while sum([drop_water(c) for c in cliffs]):
    succeeded = True
  return succeeded


def visualize():
  vis_rows = []
  for row in range(y_max+1):
    vis_rows.append(''.join([('.', '#', '~', '|')[grid[col, row]] for col in range(x_max)]))
  with open('day17-vis', 'w') as file:
    file.write('\n'.join(vis_rows))


while drop_water():
  pass

print((grid==2).sum() + (grid==-1).sum() - y_min)  # Part 1
print((grid==2).sum())  # Part 2
visualize()
