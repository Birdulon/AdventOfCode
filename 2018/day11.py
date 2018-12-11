import numpy as np
input = 4455
fuel_cells = np.zeros((300,300), dtype=np.int64)

for y in range(300):
  fuel_cells[:,y] = y+1
for x in range(300):
  fuel_cells[x,:] *= x+11
fuel_cells += input
for x in range(300):
  fuel_cells[x,:] *= x+11
fuel_cells //= 100
fuel_cells %= 10
fuel_cells -= 5

max_power = 0
max_idx = (0,0)
for x in range(298):
  for y in range(298):
    val = fuel_cells[x:x+3, y:y+3].sum()
    if val > max_power:
      max_power = val
      max_idx = (x+1,y+1)

print(max_idx)  # Part 1


max_power = 0
max_idx = (0,0,0)
for x in range(298):
  for y in range(298):
    for s in range(3, 301-max(x,y)):
      val = fuel_cells[x:x+s, y:y+s].sum()
      if  val > max_power:
        max_power = val
        max_idx = (x+1,y+1,s)

print(max_idx)  # Part 2
