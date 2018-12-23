with open('day23-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

numbers = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data]
arr = np.array(numbers, dtype=np.int64)

def nanobots_in_range_of(index):
  delta_positions = arr[:,:3] - arr[index,:3]
  distances = np.abs(delta_positions).sum(axis=1)
  return (distances <= arr[index, 3]).sum()

largest_rad_bot = arr[:,3].argmax()
print(nanobots_in_range_of(largest_rad_bot))  # Part 1


min_coords = arr[:,:3].min(axis=0)
max_coords = arr[:,:3].max(axis=0)
coords_range = max_coords - min_coords

# This is an astronomical number of potential coordinates. We can evaluate them at a resolution of 200,000 with int32s for 11GiB
def nanobots_ranging(x, y, z, downsample=1):
  delta_positions = (arr[:,:3]//downsample) - np.array((x,y,z))
  distances = np.abs(delta_positions).sum(axis=1)
  return (distances <= (arr[:,3]//downsample)).sum()


def downsample_survey(start_coords, end_coords, ds_factor):
  points_ds = np.zeros(tuple(end_coords-start_coords), dtype=np.int32)
  for x in range(start_coords[0], end_coords[0]):
    for y in range(start_coords[1], end_coords[1]):
      for z in range(start_coords[2], end_coords[2]):
        points_ds[x-start_coords[0],y-start_coords[1],z-start_coords[2]] = nanobots_ranging(x, y, z, ds_factor)
  return points_ds


ds_factor = 10000000
mins_ds = min_coords//ds_factor
maxs_ds = max_coords//ds_factor
points_ds = downsample_survey(mins_ds, maxs_ds, ds_factor)

hotspots = (np.argwhere(points_ds > points_ds.max()*0.9)+mins_ds)*ds_factor


