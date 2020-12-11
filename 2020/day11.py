import numpy as np
with open('input11', 'r') as file:
  seatmap = np.array([[c=='L' for c in line.strip()] for line in file.readlines()])

dir_slices = [np.s_[:-1,:], np.s_[:-1,:-1], np.s_[:,:-1], np.s_[1:,:-1], np.s_[1:,:], np.s_[1:,1:], np.s_[:,1:], np.s_[:-1,1:]]

def sim_step(seatmap, seatfilled):
  neighbours = np.zeros_like(seatfilled, dtype=np.int8)
  for i, dst in enumerate(dir_slices):
    src = dir_slices[(i+4)%8]
    neighbours[dst] += seatfilled[src]
  output = seatfilled.copy()
  output[(seatfilled==True) & (neighbours>=4)] = False
  output[(seatfilled==False) & (neighbours==0) & (seatmap==True)] = True
  return output

occupied_seats = seatmap & False
while(True):
  last_occ = occupied_seats.copy()
  occupied_seats = sim_step(seatmap, occupied_seats)
  if (occupied_seats == last_occ).all():
    print(f'Part 1: Occupied seats = {occupied_seats.sum()}')
    break


def sim_step_los(seatmap, seatfilled):
  neighbours = np.zeros_like(seatfilled, dtype=np.int8)
  for i, dst in enumerate(dir_slices):
    src = dir_slices[(i+4)%8]
    # Make floor propagate sight
    fill2 = seatfilled.copy()
    while(True):
      fill2old = fill2.copy()
      fill2[dst][~seatmap[dst]] |= fill2[src][~seatmap[dst]]
      if (fill2 == fill2old).all():
          break
    neighbours[dst] += fill2[src]
  output = seatfilled.copy()
  output[(seatfilled==True) & (neighbours>=5)] = False
  output[(seatfilled==False) & (neighbours==0) & (seatmap==True)] = True
  return output

occupied_seats = seatmap & False
while(True):
  last_occ = occupied_seats.copy()
  occupied_seats = sim_step_los(seatmap, occupied_seats)
  if (occupied_seats == last_occ).all():
    print(f'Part 2: Occupied seats = {occupied_seats.sum()}')
    break
