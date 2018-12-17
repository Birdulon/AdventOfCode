with open('day17-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

# numbers = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data]
Xmin = [int(re.findall(r'x=(\d+)', d)[0]) for d in data]
Xmax = [int(re.findall(r'x=(?:\d+\.\.)?(\d+)', d)[0]) for d in data]
Ymin = [int(re.findall(r'y=(\d+)', d)[0]) for d in data]
Ymax = [int(re.findall(r'y=(?:\d+\.\.)?(\d+)', d)[0]) for d in data]

# arr = np.array(numbers, dtype=np.int64)
#
# # x, y_start, y_end
#
y_min = min(Ymin)
y_max = max(Ymax)

x_max = 700

init_grid = np.zeros((x_max, y_max), dtype=np.int64)  # 0 = Sand, 1 = Clay, 2 = water
spring = [500, 0]

for xmin, xmax, ymin, ymax in zip(Xmin, Xmax, Ymin, Ymax):
  init_grid[xmin:xmax+1, ymin:ymax+1] = 1

grid = init_grid.copy()

def drop_water(source=spring):
  x, y = source
  print('Dropping water from', source)
  surface = grid[x, y:].argmax()
  if surface == 0:
    return False
    # raise ValueError('Out of bounds')
  surface_y = surface + y - 1
  # Find walls left and right
  wall_left = (grid[x:0:-1, surface_y] > 0).argmax()
  wall_right = (grid[x:, surface_y] > 0).argmax()
  if wall_left:
    left_x = x - wall_left + 1
    cliff = (grid[x:left_x-1:-1, surface_y + 1] == 0).argmax()
    if cliff:
      print('Found left wall but cliff present')
      wall_left = False
  if wall_right:
    right_x = x + wall_right #- 1
    cliff = (grid[x:right_x, surface_y+1] == 0).argmax()
    if cliff:
      print('Found right wall but cliff present')
      wall_right = False

  if wall_right and wall_left:
    # Fill level of basin
    grid[left_x:right_x, surface_y] = 2
    return True
  sub_returns = False
  if not wall_left:
    cliff = (grid[x:0:-1, surface_y+1] == 0).argmax()
    if cliff:
      # Drop off the left
      sub_returns |= drop_water((x - cliff, surface_y))
  if not wall_right:
    cliff = (grid[x:, surface_y+1] == 0).argmax()
    if cliff:
      # Drop off the right
      sub_returns |= drop_water((x + cliff, surface_y))

  return sub_returns



def visualize():
  vis_rows = []
  for row in range(y_max):
    vis_rows.append(''.join([('.', '#', '~')[grid[col, row]] for col in range(x_max)]))

  with open('day17-vis', 'w') as file:
    file.write('\n'.join(vis_rows))

# arr is all clay shelves

# drop_water((502, 35))


# 14572 low
# 15414 low
# 23233 low ??????
