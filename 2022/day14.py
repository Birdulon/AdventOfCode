from helpers import *
lines = read_day(day).split('\n')
sample_lines = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''.strip().split('\n')

AIR = ord('.')
ROCK = ord('#')
SAND_SOURCE = ord('+')
SAND_REST = ord('o')
SAND_ORIGIN = (500, 0)
FALL_DIRS = np.array([[0,1], [-1,1], [1,1]], dtype=dtype)

def apply_sand_fall(map: ArrayLike) -> bool:
	falling_sand_pos = np.array(SAND_ORIGIN, dtype=dtype)
	MAX_Y = map.shape[1] - 1
	while falling_sand_pos[1] < MAX_Y:
		for dir in FALL_DIRS:
			if map[*(falling_sand_pos + dir)] == AIR:
				falling_sand_pos += dir
				break
		else:
			if falling_sand_pos[1] == 0:
				return False
			# resting place
			# print('Resting at', falling_sand_pos)
			map[*falling_sand_pos] = SAND_REST
			return True
	return False

def sim(lines: list[str], solid_floor=False) -> ArrayLike:
	nums = [[int(x) for x in numbers_pattern.findall(line)] for line in lines]
	max_x = max([max(n[::2]) for n in nums])
	max_y = max([max(n[1::2]) for n in nums])
	print(f'Max X: {max_x}, Max Y: {max_y}')
	dim_x = max_x + max_y  # assume it can pile out diagonally all the way
	map = np.full((dim_x,max_y+4), AIR, dtype=np.uint8)
	for n in nums:
		for x0,y0,x1,y1 in zip(n[::2], n[1::2], n[2::2], n[3::2]):
			map[min(x0,x1):max(x0,x1)+1, min(y0,y1):max(y0,y1)+1] = ROCK
	if solid_floor:
		map[:,max_y+2] = ROCK
	map[SAND_ORIGIN] = SAND_SOURCE
	while apply_sand_fall(map):
		pass
	return map

def visualize_map(map: ArrayLike):
	X, Y = np.nonzero(map == SAND_REST)
	x0 = max(min(X) - 2, 0)
	x1 = min(max(X) + 3, map.shape[0])
	y0 = max(min(Y) - 2, 0)
	y1 = min(max(Y) + 3, map.shape[1])
	for row in map[x0:x1, y0:y1].T:
		print(''.join((chr(x) for x in row)))


map_1 = sim(lines)  # 885
map_2 = sim(lines, True)  # 28690 (+1)
print(f'Part 1: {(map_1==SAND_REST).sum()}')
print(f'Part 2: {(map_2==SAND_REST).sum()+(map_2==SAND_SOURCE).sum()}')
if input('Print Part 1 visualization? [y/N]: ').lower() == 'y':
	visualize_map(map_1)
	print()
if input('Print Part 2 visualization? [y/N]: ').lower() == 'y':
	visualize_map(map_2)
