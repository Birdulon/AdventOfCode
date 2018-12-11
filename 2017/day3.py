input = 312051
import numpy as np

num_rings = 1000
rings_sizes = np.empty(num_rings, dtype=np.int64)

rings_sizes[0] = 1
for i in range(1, num_rings):
  rings_sizes[i] = 8*i

rings_ends = rings_sizes.cumsum()

def find_position(number):
  ring_idx = (rings_ends >= number).argmax()
  pos_on_ring = number - rings_ends[ring_idx-1] if ring_idx > 0 else 1
  return ring_idx, pos_on_ring

def distance(number):
  ring_idx, pos_on_ring = find_position(number)
  ring_pos_dist = abs(pos_on_ring%(ring_idx*2)-ring_idx)
  return ring_idx + ring_pos_dist

print(distance(input))  # Part 1


mem_plane_rings = 20
mp_offset = mem_plane_rings
mp_size = mem_plane_rings*2+1
mem_plane = np.zeros((mp_size, mp_size), dtype=np.int64)

directions = np.array([[0,1], [-1,0], [0,-1], [1,0]], dtype=np.int32)
direction = -1
position = np.array((mp_offset, mp_offset), dtype=np.int32)
mem_plane[mp_offset, mp_offset] = 1
for i in range((mp_size-2)**2):
  if mem_plane[tuple(position + directions[(direction+1)%4])] == 0:
    direction = (direction+1) % 4
  position += directions[direction]
  x, y = position
  mem_plane[x,y] = mem_plane[x-1:x+2, y-1:y+2].sum()
  if mem_plane[x,y] > input:
    print(mem_plane[x,y])  # Part 2
    break



