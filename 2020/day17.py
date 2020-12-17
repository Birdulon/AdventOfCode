import numpy as np
with open('input17', 'r') as file:
  init_state = np.array([[c == '#' for c in l.strip()] for l in file.readlines()])

def sim_step3d(state):
  new_state = set()
  neighbours = {}
  for (x,y,z) in state:
    for i in (-1,0,1):
      for j in (-1,0,1):
        for k in (-1,0,1):
          neighbours[(x+i,y+j,z+k)] = neighbours.get((x+i,y+j,z+k), 0) + 1
  for loc, n in neighbours.items():
    if loc in state:
      if n in (3,4):  # We added an off-by-one by counting active cubes as their own neighbour for simplicity
          new_state.add(loc)
    elif n == 3:
      new_state.add(loc)
  return new_state

state = {(x,y,0) for (x, y), v in np.ndenumerate(init_state) if v}
for i in range(6):
  state = sim_step3d(state)
print(f'Part 1: {len(state)}')


def sim_step4d(state):
  new_state = set()
  neighbours = {}
  for (x,y,z,u) in state:
    for i in (-1,0,1):
      for j in (-1,0,1):
        for k in (-1,0,1):
          for l in (-1,0,1):
            neighbours[(x+i,y+j,z+k,u+l)] = neighbours.get((x+i,y+j,z+k,u+l), 0) + 1
  for loc, n in neighbours.items():
    if loc in state:
      if n in (3,4):  # We added an off-by-one by counting active cubes as their own neighbour for simplicity
        new_state.add(loc)
    elif n == 3:
      new_state.add(loc)
  return new_state


state = {(x,y,0,0) for (x, y), v in np.ndenumerate(init_state) if v}
for i in range(6):
    state = sim_step4d(state)
print(f'Part 2: {len(state)}')
