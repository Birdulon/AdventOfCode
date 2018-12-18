with open('day18-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np

WIDTH = len(data)
HEIGHT = len(data[0])
init_grid = np.zeros((WIDTH+2, HEIGHT+2), dtype=np.int64)
objects = {'.': 0, '|': 1, '#': 2}

for y, row in enumerate(data):
  for x, c in enumerate(row):
    init_grid[x+1,y+1] = objects[c]
grid = init_grid.copy()


def do_round():
  global grid
  new_grid = np.zeros_like(grid)
  for y in range(1, HEIGHT+1):
    for x in range(1, WIDTH+1):
      ex = grid[x, y]
      square = grid[x-1:x+2, y-1:y+2]
      new = ex
      if ex == 0 and (square == 1).sum() >= 3:
        new = 1
      elif ex == 1 and (square == 2).sum() >= 3:
        new = 2
      elif ex == 2 and not ( (square == 2).sum() >= 2 and (square == 1).sum() > 0 ):
        new = 0
      new_grid[x, y] = new
  grid[:] = new_grid[:]

for i in range(10):
  do_round()

print((grid == 2).sum() * (grid == 1).sum())  # Part 1

past_values = np.zeros(10000, dtype=np.int64)
grid[:] = init_grid[:]

for i in range(1000000000):
  past_values[i] = (grid == 2).sum() * (grid == 1).sum()
  m = (past_values == past_values[i-1])
  if m.sum() > 1:
    j = m.argmax()
    if past_values[i] == past_values[j+1]:
      cycle_length = i-j-1
      print(f'Cycle found from {j} to {i-1} minutes! Length {cycle_length} minutes.')
      value = past_values[j + ((1000000000-j)%cycle_length)]
      print(f'After 1000000000 minutes, value will be {value}')  # Part 2
      break
  do_round()
