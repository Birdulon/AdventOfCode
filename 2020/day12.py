import numpy as np
with open('input12', 'r') as file:
  input = [line.strip() for line in file.readlines()]

directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])

position = np.array([0,0])
direction = 0

def move_dir(direction, x):
  global position, directions
  position += x*directions[direction]

def rotate(degrees):
  global direction
  direction = (direction + degrees//90)%4

moves = {
  'F': lambda x: move_dir(direction, x),
  'E': lambda x: move_dir(0, x),
  'N': lambda x: move_dir(1, x),
  'W': lambda x: move_dir(2, x),
  'S': lambda x: move_dir(3, x),
  'L': lambda x: rotate(x),
  'R': lambda x: rotate(-x),
}

# position = np.array([0,0])
for line in input:
  moves[line[0]](int(line[1:]))
print(f'Part 1: {position} - manhattan distance = {sum(abs(position))}')


waypoint = np.array([10, 1])
position = np.array([0,0])

def move_waypoint(direction, x):
  global waypoint
  waypoint += x*directions[direction]

def rotate_waypoint(degrees):
  global waypoint
  waypoint = np.ravel(waypoint * pow(np.mat([[0, 1],[-1, 0]]), (degrees//90)%4))

def move_to_waypoint(x):
  global position
  position += waypoint * x

moves_wp = {
  'F': lambda x: move_to_waypoint(x),
  'E': lambda x: move_waypoint(0, x),
  'N': lambda x: move_waypoint(1, x),
  'W': lambda x: move_waypoint(2, x),
  'S': lambda x: move_waypoint(3, x),
  'L': lambda x: rotate_waypoint(x),
  'R': lambda x: rotate_waypoint(-x),
}

for line in input:
  moves_wp[line[0]](int(line[1:]))
print(f'Part 2: {position} - manhattan distance = {sum(abs(position))}')
