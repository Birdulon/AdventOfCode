import numpy as np
with open('input/09', 'r') as file:
	lines = file.read().strip().split('\n')
dtype = np.int32

directions_array = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=dtype)
directions_dict = {'R': directions_array[0], 'L': directions_array[1], 'D': directions_array[2], 'U': directions_array[3]}  # Positive down for visualization

def move_tail(rope: np.array):
	for i in range(1, rope.shape[0]):
		dx, dy = rope[i-1,:] - rope[i,:]
		if abs(dx) > 1 and dy == 0:
			rope[i,0] += 1 if dx > 0 else -1
		elif abs(dy) > 1 and dx == 0:
			rope[i,1] += 1 if dy > 0 else -1
		elif abs(dx) + abs(dy) > 2:
			rope[i,0] += 1 if dx > 0 else -1
			rope[i,1] += 1 if dy > 0 else -1

def simulate_rope_drag(length: int, lines: list[str]):
	rope = np.zeros([length,2], dtype=dtype)
	visited = {(rope[-1,0], rope[-1,1])}
	for line in lines:
		dir_vector = directions_dict[line[0]]
		amount = int(line[2:])
		for i in range(amount):
			rope[0,:] += dir_vector
			move_tail(rope)
			visited.add((rope[-1,0], rope[-1,1]))
	return visited

def visualise_cells(visited: set, size=20):
	vis_lol = [['#' if (x,y) in visited else '.' for x in range(-size, size)] for y in range(-size, size)]
	vis_str = '\n'.join(''.join(line) for line in vis_lol)
	print(vis_str)


visited_part_1 = simulate_rope_drag(2, lines)
print(f'Part 1: String length of 2 - tail visits {len(visited_part_1)} cells')
visited_part_2 = simulate_rope_drag(10, lines)
print(f'Part 2: String length of 10 - tail visits {len(visited_part_2)} cells')

if input('Visualise part 1 cells? [y/N]: ').lower() == 'y':
	visualise_cells(visited_part_1, 70)
	print()
if input('Visualise part 2 cells? [y/N]: ').lower() == 'y':
	visualise_cells(visited_part_2, 70)
