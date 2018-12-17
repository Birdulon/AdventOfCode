with open('day15-input-dev', 'r') as file:
  data = [l.strip('\n') for l in file]
# data = [
# '#######',
# '#.G...#',
# '#...EG#',
# '#.#.#G#',
# '#..G#E#',
# '#.....#',
# '#######',
# ]
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder
import sys

grid = np.zeros((len(data), len(data[0])), dtype=np.int64)
cells = {'#': 0, '.': 1, 'G': 1, 'E': 1}
goblins = []
elves = []
starting_hp = 200
starting_atk = 3
starting_atk_elf = 29
adjacent = np.array([[0,-1], [-1,0], [1,0], [0,1]], dtype=np.int64)
enemy_teams = [goblins, elves]
unit_positions = []
pathfind_grid = None
# pathfinder = AStarFinder()
pathfinder = DijkstraFinder()
UID = 0

class Unit:
  def __init__(self, x, y, starting_hp, atk, team):
    global UID
    self.team = team
    self.atk = atk
    self.hp = starting_hp
    self.pos = np.array([x, y], dtype=np.int64)
    self.uid = UID
    UID += 1

  def __eq__(self, other):
    return self.uid == other.uid

  @property
  def x(self):
    return self.pos[0]
  @property
  def y(self):
    return self.pos[1]

  def distance(self, pos):
    return np.abs(pos - self.pos).sum()

  def path_to(self, pos, exhaustive=False):
    if not exhaustive:
      pathfind_grid = Grid(matrix=grid2)
      start = pathfind_grid.node(*tuple(self.pos))
      end = pathfind_grid.node(*tuple(pos))
      path, runs = pathfinder.find_path(start, end, pathfind_grid)
      return path
    else:
      paths = []
      for d in range(len(adjacent)):
        try:
          trystart = tuple(self.pos + adjacent[d])
          if grid2[trystart] and trystart not in unit_positions:
            pathfind_grid = Grid(matrix=grid2.T)
            start = pathfind_grid.node(*trystart)
            end = pathfind_grid.node(*tuple(pos))
            path, runs = pathfinder.find_path(start, end, pathfind_grid)
            # print(pathfind_grid.grid_str(path=path, start=start, end=end))
            if len(path) > 0:
              paths.append(path)
        except Exception:
          pass
      if paths:
        paths = sorted(paths, key=lambda x: len(x))
        # print(paths)
        return paths[0]
      return []

  def path_distance(self, pos):
    return len(self.path_to(pos, True)) or 90000  # Sorting hack

  def path_distance_and_priority(self, pos):
    path = self.path_to(pos, True)
    if path:
      for i in range(len(adjacent)):
        if path[0] == tuple(self.pos + adjacent[i]):
          priority = i
          break
      return len(path), priority
    return (90000, 90000)  # Sorting hack

  def __repr__(self):
    return f'[{"Elf" if not self.team else "Gob"}, Position {self.x},{self.y}, HP {self.hp}]'


for y, row in enumerate(data):
  for x, c in enumerate(row):
    grid[x,y] = cells[c]
    if c == 'E':
      elves.append(Unit(x, y, starting_hp, starting_atk_elf, 0))
    elif c == 'G':
      goblins.append(Unit(x, y, starting_hp, starting_atk, 1))
grid2 = grid.copy()

def turn_sort(unit):
  return unit.y, unit.x


def target_sort(unit):
  return unit.hp, unit.y, unit.x


def do_round():
  global unit_positions, pathfind_grid
  combatants = sorted(goblins + elves, key=turn_sort)
  i = 0
  while i < len(combatants):
    unit_positions = [tuple(u.pos) for u in combatants]
    grid2[:] = grid[:]
    for p in unit_positions:
      grid2[p] = -1
    unit = combatants[i]
    i += 1
    enemy_team = enemy_teams[unit.team]

    # If no enemies left, end combat
    if len(enemy_team) == 0:
      return

    # If adjacent to an enemy, attack it
    adjacent_enemies = []
    for enemy in enemy_team:
      if unit.distance(enemy.pos) == 1:
        adjacent_enemies.append(enemy)
    if adjacent_enemies:
      # print(sorted(adjacent_enemies, key=target_sort))
      target = sorted(adjacent_enemies, key=target_sort)[0]
      # print(f'Unit #{unit.uid} attacking unit {target.uid}')
      target.hp -= unit.atk
      if target.hp <= 0:
        if target.team == 0:
          print('Elf died, aborting!')
          sys.exit(1)
        enemy_team.remove(target)
        j = combatants.index(target)
        combatants.pop(j)
        if j < i:
          i -= 1
      continue

    # Find all cells to move to
    target_cells = {tuple(t.pos + adjacent[j]) for t in enemy_team for j in range(4)}
    target_cells = {c for c in target_cells if grid[c] == 1 and c not in unit_positions}
    target_cells = sorted([np.array(c) for c in target_cells], key=lambda x: unit.path_distance_and_priority(x))
    # Move to closest target cell
    if target_cells:
      path = unit.path_to(target_cells[0], exhaustive=True)
      if path:
        # print(f'Unit #{unit.uid} moving from {unit.pos} to {path[0]}')
        unit.pos[:] = path[0]
      else:
        pass
        # print(f'Unit #{unit.uid} cannot move!')

    # If adjacent to an enemy, attack it
    adjacent_enemies = []
    for enemy in enemy_team:
      if unit.distance(enemy.pos) == 1:
        adjacent_enemies.append(enemy)
    if adjacent_enemies:
      target = sorted(adjacent_enemies, key=target_sort)[0]
      # print(f'Unit #{unit.uid} attacking unit {target.uid}')
      target.hp -= unit.atk
      if target.hp <= 0:
        enemy_team.remove(target)
        j = combatants.index(target)
        combatants.pop(j)
        if j < i:
          i -= 1
      continue

def print_state():
  char_array = np.zeros_like(grid)
  char_array[(grid == 0)] = ord('#')
  char_array[(grid == 1)] = ord('.')
  unit_strs = [[] for i in range(len(char_array))]
  for g in goblins:
    char_array[g.x, g.y] = ord('G')
    unit_strs[g.y].append((f'G({g.hp})', g.x))
  for e in elves:
    char_array[e.x, e.y] = ord('E')
    unit_strs[e.y].append((f'E({e.hp})', e.x))
  for row in range(len(char_array)):
    maprow =''.join([chr(c) for c in char_array.T[row]])
    unithps = ', '.join([s[0] for s in sorted(unit_strs[row], key=lambda x: x[1])])
    print(maprow, unithps)



def do_exterminatus(quit_after=9999999):
  rounds = 0
  while len(goblins) and len(elves) and rounds < quit_after:
    print(f'Round #{rounds}')
    print_state()
    do_round()
    rounds += 1
  return rounds


round = do_exterminatus()
if goblins:
  num = sum(u.hp for u in goblins)
else:
  num = sum(u.hp for u in elves)
print(round, num, round*num)
