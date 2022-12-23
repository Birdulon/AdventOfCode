from helpers import *
lines = read_day(23).split('\n')
sample_lines = '''
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''.strip().split('\n')

def get_intention(round, elves, x, y):
	adj_nw = (x-1,y-1) in elves
	adj_w = (x-1,y) in elves
	adj_sw = (x-1,y+1) in elves
	adj_n = (x,y-1) in elves
	adj_s = (x,y+1) in elves
	adj_ne = (x+1,y-1) in elves
	adj_e = (x+1,y) in elves
	adj_se = (x+1,y+1) in elves
	if adj_nw or adj_n or adj_ne or adj_w or adj_e or adj_sw or adj_s or adj_se:
		for i in range(4):
			direction = (round + i) % 4
			if (direction == 0) and not (adj_n or adj_nw or adj_ne):
				return (x,y-1)  # move north
			if (direction == 1) and not (adj_s or adj_sw or adj_se):
				return (x,y+1)  # move south
			if (direction == 2) and not (adj_w or adj_nw or adj_sw):
				return (x-1,y)  # move west
			if (direction == 3) and not (adj_e or adj_ne or adj_se):
				return (x+1,y)  # move east
	return (x,y)  # no movement

def simulate(lines: list[str], rounds: int = 10) -> set[tuple[int,int]]:
	# position = np.array([[c=='#' for c in line] for line in lines], dtype=np.bool8)
	elves = set()
	for row, line in enumerate(lines):
		for col, c in enumerate(line):
			if c == '#':
				elves.add((col, row))

	for round in range(rounds):
		if round == 10:
			print(f'*** Part 1: ground tiles after round #10: {get_rect(elves)} ***')
		# else:
		# 	print(f'\tground tiles before round #{round+1}: {get_rect(elves)}')
		# print(f'performing round #{round+1}')
		next_elves = {}
		for x,y in sorted(elves, key=lambda p: (p[1], p[0])):
			intention = get_intention(round, elves, x, y)
			# print(f'{x,y} wants to move to {intention}')
			next_elves[intention] = next_elves.get(intention, []) + [(x,y)]
		old_elves = elves
		elves = set()
		for position, elf_intentions in next_elves.items():
			if len(elf_intentions) == 1:
				elves.add(position)
			else:
				# print(f'conflict: {len(elf_intentions)} elves tried to move to {position}')
				elves |= set(elf_intentions)  # neither move
		if old_elves == elves:
			print(f'*** Part 2: No elves moved in round #{round+1} ***')
			break
	print(f'Final ground tiles: {get_rect(elves)}')
	return elves

def get_rect(elves: set[tuple[int,int]]):
	x0, x1, y0, y1 = None, None, None, None
	for x,y in elves:
		if x0 is None or x < x0:
			x0 = x
		if x1 is None or x > x1:
			x1 = x
		if y0 is None or y < y0:
			y0 = y
		if y1 is None or y > y1:
			y1 = y
	# print(f'Elves in rectangle from x:{x0}~{x1}, y:{y0}~{y1}')
	# for y in range(y0, y1+1):
	# 	print(''.join(('#' if (x,y) in elves else '.' for x in range(x0,x1+1))))
	rect_size = (x1-x0+1)*(y1-y0+1)  # inclusive
	return rect_size - len(elves)

simulate(sample_lines, 100)
simulate(lines, 100000)
