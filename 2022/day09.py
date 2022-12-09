from helpers import *
lines = read_day(9).split('\n')

def move_tail(rope: ArrayLike):
	for i in range(1, rope.shape[0]):
		delta = rope[i-1] - rope[i]
		abs_delta = abs(delta)
		if (abs_delta.max() > 1 and abs_delta.min() == 0) or (sum(abs_delta) > 2):
			rope[i] += np.sign(delta)

def simulate_rope_drag(length: int, lines: list[str]):
	rope = np.zeros([length,2], dtype=dtype)
	visited = {tuple(rope[-1])}
	for line in lines:
		dir_vector = directions_dict[line[0]]
		amount = int(line[2:])
		for i in range(amount):
			rope[0] += dir_vector
			move_tail(rope)
			visited.add(tuple(rope[-1]))
	return visited


visited_part_1 = simulate_rope_drag(2, lines)
print(f'Part 1: String length of 2 - tail visits {len(visited_part_1)} cells')
visited_part_2 = simulate_rope_drag(10, lines)
print(f'Part 2: String length of 10 - tail visits {len(visited_part_2)} cells')

if input('Visualise part 1 cells? [y/N]: ').lower() == 'y':
	visualise_sparse_cells_set(visited_part_1, 70)
	print()
if input('Visualise part 2 cells? [y/N]: ').lower() == 'y':
	visualise_sparse_cells_set(visited_part_2, 70)
