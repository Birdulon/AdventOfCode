import numpy as np
with open('input03', 'r') as file:
  treemap = np.array([[c=='#' for c in line.strip()] for line in file.readlines()])
rows, cols = treemap.shape
r = np.arange(rows)
print(f'Part 1: {treemap[r, (r*3)%cols].sum()} trees hit')

slopes = [(1,1), (1,3), (1,5), (1,7), (2,1)]
tps = [treemap[np.arange(0, rows, i), (np.arange(-(-rows//i))*j)%cols].sum() for i,j in slopes]
print(f'Part 2: {"*".join([str(t) for t in tps])} = {np.prod(tps)}')
