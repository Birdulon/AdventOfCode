import numpy as np
input = 4455
fuel_cells = np.zeros((301,301), dtype=np.int64)

for y in range(1, 301):
  fuel_cells[1:,y] = y
for x in range(1, 301):
  fuel_cells[x,1:] *= x+10
fuel_cells[1:,1:] += input
for x in range(1, 301):
  fuel_cells[x,1:] *= x+10
fuel_cells[1:,1:] //= 100
fuel_cells[1:,1:] %= 10
fuel_cells[1:,1:] -= 5
fuel_cs = fuel_cells.cumsum(axis=0).cumsum(axis=1)


def sum_square(x, y, s):
  A = fuel_cs[x-1, y-1]
  B = fuel_cs[x+s-1, y-1]
  C = fuel_cs[x-1, y+s-1]
  D = fuel_cs[x+s-1, y+s-1]
  return D - B - C + A


max_power_3 = 0
max_idx_3 = (0, 0, 0)
for x in range(1, 299):
  for y in range(1, 299):
    val = sum_square(x, y, 3)
    if val > max_power_3:
      max_power_3 = val
      max_idx_3 = (x, y, 3)

print(max_idx_3)  # Part 1


max_power_s = 0
max_idx_s = (0,0,0)
for x in range(1, 298):
  for y in range(1, 298):
    for s in range(4, 302-max(x, y)):
      val = sum_square(x, y, s)
      if val > max_power_s:
        max_power_s = val
        max_idx_s = (x, y, s)

print(max_idx_s)  # Part 2
