with open('day25-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

numbers = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data]
arr = np.array(numbers, dtype=np.int64)
max_constellation_radius = 3
constellation_ids = np.arange((len(arr)), dtype=np.int64)


def points_in_range_of(index):
  distances = np.abs(arr - arr[index]).sum(axis=1)
  return np.argwhere(distances <= max_constellation_radius)[:,0]  # Note this will include the point itself


for i in range(len(arr)):
  points = points_in_range_of(i)
  constellations_to_merge = constellation_ids[points]
  constellation_id = constellation_ids[points].min()
  for c in constellations_to_merge:
    constellation_ids[constellation_ids == c] = constellation_id

print(len(np.unique(constellation_ids)))  # Part 1
