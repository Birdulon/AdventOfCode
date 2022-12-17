from helpers import *

gas_cycles = read_day(17)
sample_gas_cycles = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

rocks = '''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''.strip().split('\n\n')
# rock_shapes = [np.array([[1 if c=='#' else 0 for c in line] for line in r.split('\n')], dtype=np.int8).T for r in rocks]
rock_shapes = [np.fliplr(np.array([[1 if c=='#' else 0 for c in line] for line in r.split('\n')], dtype=np.int8).T) for r in rocks]

def simulate_rockfall(gas_cycle: str, num_rocks=50000, debug=False) -> ArrayLike:  # returns height increment per rock
	def p(message):
		if debug:
			print(message)

	width = 7
	height_5_rocks = 1+3+3+4+2
	max_possible_height = (num_rocks//5 + 2) * height_5_rocks
	len_gas_cycle = len(gas_cycle)

	field = np.zeros((7, max_possible_height), dtype=np.int8)
	height_increments = np.zeros(num_rocks, dtype=np.int8)
	highest = 0
	t = -1
	for r in range(num_rocks):
		rock_shape = rock_shapes[r%5]
		r_width, r_height = rock_shape.shape

		def check_collision(r_x, r_y):
			r_x2 = r_x + r_width
			r_y2 = r_y + r_height
			if r_x < 0:
				p(f'would hit left wall - {r_x, r_x2} at y={r_y}')
				return True
			if r_x2 > width:
				p(f'would hit right wall - {r_x, r_x2} at y={r_y}')
				return True
			if r_y < 0:
				p(f'would hit floor - {r_x, r_x2} at y={r_y}')
				return True
			return np.any(field[r_x:r_x2, r_y:r_y2] & rock_shape == 1)

		# Spawn rock with bottom-left corner at x=2, y=highest+3  (y-up)
		r_x = 2
		r_y = highest + 3 
		while True:
			t += 1
			if gas_cycle[t%len_gas_cycle] == '>':
				if not check_collision(r_x+1, r_y):  # move right
					r_x += 1
					p('moved right')
			else:
				if not check_collision(r_x-1, r_y):  # move left
					r_x -= 1
					p('moved left')
			# move down
			if check_collision(r_x, r_y-1):
				field[r_x:r_x+r_width, r_y:r_y+r_height] |= rock_shape
				old_highest = highest
				highest = max(highest, r_y+r_height)
				height_increments[r] = highest - old_highest
				break
			else:
				r_y -= 1
				p('moved down')
		p(f'rock #{r} landed, highest point {highest}, gas cycle {t}, rock shape ({r_width}x{r_height}) at {r_x},{r_y}')
	return height_increments

sample_incs = simulate_rockfall(sample_gas_cycles, 10000)
incs = simulate_rockfall(gas_cycles, 30000)
print(f'Part 1 (sample): {sample_incs[:2022].sum()}')
print(f'Part 1: {incs[:2022].sum()}')


def find_cycle_and_infer(increments: ArrayLike, search_cycle_length: int, target_index: int):
	search_term = increments[search_cycle_length:search_cycle_length*2]
	hits = []
	for st in range(search_cycle_length*2, len(increments)-search_cycle_length):
		if np.all(increments[st:st+search_cycle_length] == search_term):
			hits.append(st)
			print(f'Found loop starting at {st}')
			if len(hits) > 2:
				break
	else:
		print('no loop found!')
		return

	loop_len = hits[1]-hits[0]
	loop_len2 = hits[2]-hits[1]
	if loop_len2 == loop_len:
		print(f'Confirmed loop of length {loop_len}')
	else:
		print(f'Mismatched loop lengths of {loop_len} and {loop_len2}!')
		return

	base_value = increments[:hits[0]].sum()
	loop_values = increments[hits[0]:hits[1]].cumsum()
	loop_total = loop_values[-1]

	loops, remainder = divmod(target_index - hits[0], loop_len)
	value = base_value + loop_total*loops
	if remainder > 0:
		value += loop_values[remainder-1]
	return value

print(f'Part 2 (sample): {find_cycle_and_infer(sample_incs, 1000, 1000000000000)}')
print(f'Part 2: {find_cycle_and_infer(incs, 5000, 1000000000000)}')
