from helpers import *
input_map, _, input_directions = read_day(22, False).partition('\n\n')
input_map = input_map.split('\n')

sample_map, _, sample_directions = '''
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''.strip('\n').partition('\n\n')
sample_map = sample_map.split('\n')

instruction_regex = re.compile(r'((?:\d+)|[RL])')
# print(instruction_regex.findall(sample_directions))
def navigate(input_map: list[str], input_directions: str) -> int:
	height = len(input_map)
	print(f'height is {height}')
	directions = instruction_regex.findall(input_directions)
	y = 0
	x = input_map[y].index('.')
	print(input_map[y])
	print(input_map[-1])
	facing = 0  # clockwise
	for direction in directions:
		# print(x, y, facing)
		if direction == 'L':
			facing = (facing-1) % 4
		elif direction == 'R':
			facing = (facing+1) % 4
		else:
			steps = int(direction)
			# print(f'moving {steps} steps in facing {facing}')
			if facing == 0:  # Right ->
				row = input_map[y]
				for i in range(steps):
					nx = x + 1
					if nx >= len(row) or row[nx] == ' ':  # wrap around
						first_row_wall = 1_000_000
						try:
							first_row_wall = row.index('#')
						except:
							print(f'no wall in row {y}, moving to {row.index(".")}')
							print(row)
							pass
						first_row_space = 1_000_000
						try:
							first_row_space = row.index('.')
						except:
							print(f'no space in row {y}')
							pass
						if first_row_wall <= first_row_space:
							# print('hit wrapped wall')
							break
						else:
							x = first_row_space
					elif row[nx] == '#':  # wall, stop
						# print('hit wall')
						break
					else:
						x = nx
				# print('finished moving right')
			elif facing == 2:  # Left <-
				row = input_map[y]
				for i in range(steps):
					nx = x - 1
					if nx < 0 or row[nx] == ' ':  # wrap around
						nx = len(row) - 1
						if row[nx] == '#':
							# print('hit wrapped wall wrapping left')
							break
						else:
							print(f'wrapping left on row {y} - from {x} to {nx}')
							x = nx
					elif row[nx] == '#':  # wall, stop
						break
					else:
						x = nx
			elif facing == 1:  # Down v
				for i in range(steps):
					ny = y + 1
					if ny >= height or x >= len(input_map[ny]) or input_map[ny][x] == ' ':  # wrap around
						result = None
						for r, row in enumerate(input_map):
							if len(row) > x and row[x] != ' ':
								if row[x] == '#':
									break
								else:
									result = r
									break
						if result is None:
							break
						else:
							y = result
					elif input_map[ny][x] == '#':  # wall, stop
						break
					else:
						y = ny
			elif facing == 3:  # Up ^
				for i in range(steps):
					ny = y-1
					if ny < 0 or x >= len(input_map[ny]) or input_map[ny][x] == ' ':  # wrap around
						result = None
						for r, row in enumerate(reversed(input_map)):
							if len(row) > x and row[x] != ' ':
								if row[x] == '#':
									break
								else:
									print(f'wrapping up from {y} to {r}')
									result = height-1-r
									break
						if result is None:
							break
						else:
							y = result
					elif input_map[ny][x] == '#':  # wall, stop
						break
					else:
						y = ny
	print(x, y, facing)
	return 1000*(y+1) + 4*(x+1) + facing

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
def navigate_cube(input_map: list[str], input_directions: str, square_size=50) -> int:
	# Map is laid out like
	#    14
	#    2
	#   53
	#   6
	# So  (5 opposite 4) (1 opposite 3) (2 opposite 6)
	# def tile(i: int, offset: int = 0, rev_offset: bool = False) -> int:
	# 	o = offset % square_size
	# 	base = i * square_size
	# 	if rev_offset:
	# 		return base + (square_size-1) - o
	# 	return base + o

	def edge_wrap(x, y, facing, i, j, next_facing):
		# Get position along edge
		if facing == RIGHT:
			position = y % square_size
		elif facing == DOWN:
			position = x % square_size
		elif facing == LEFT:
			position = (square_size - 1) - (y % square_size)
		elif facing == UP:
			position = (square_size - 1) - (x % square_size)
		# Align this position to new edge
		if next_facing == RIGHT:
			return (i*square_size), ((j+1)*square_size - 1 - position), next_facing
		elif next_facing == DOWN:
			return ((i+1)*square_size - 1 - position), (j*square_size), next_facing
		elif next_facing == LEFT:
			return ((i+1)*square_size - 1), (j*square_size + position), next_facing
		elif next_facing == UP:
			return (i*square_size + position), ((j+1)*square_size - 1), next_facing
		# if next_facing == RIGHT:
		# 	return (i*square_size), (j*square_size + position), next_facing
		# elif next_facing == DOWN:
		# 	return (i*square_size + position), (j*square_size), next_facing
		# elif next_facing == LEFT:
		# 	return ((i+1)*square_size - 1), ((j+1)*square_size - 1 - position), next_facing
		# elif next_facing == UP:
		# 	return ((i+1)*square_size - 1 - position), ((j+1)*square_size - 1), next_facing



	height = len(input_map)
	print(f'height is {height}')
	directions = instruction_regex.findall(input_directions)
	y = 0
	x = input_map[y].index('.')
	print(input_map[y])
	print(input_map[-1])
	facing = 0  # clockwise
	for direction in directions:
		# print(x, y, facing)
		if direction == 'L':
			print('turning L')
			facing = (facing-1) % 4
		elif direction == 'R':
			print('turning R')
			facing = (facing+1) % 4
		else:
			steps = int(direction)
			for i in range(steps):
				# print(x,y,facing)
				print(f'Tile ({x//square_size},{y//square_size}) Offset ({x%square_size},{y%square_size}) Facing {facing} [{x},{y}]')
				nx, ny, n_facing = x, y, facing
				if facing == 0:  # Right ->
					nx = x + 1
					if nx >= len(input_map[y]) or input_map[y][nx] == ' ':  # wrap around
						# 14
						# 2
						#53
						#6
						if y < square_size:
							print('going right from 4 wraps to the right of 3 (right -> left)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 2, LEFT)
						if y < 2*square_size:
							print('going right from 2 wraps to the bottom of 4 (right -> up)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 2, 0, UP)
						elif y < 3*square_size:
							print('going right from 3 wraps to the right of 4 (right -> left)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 2, 0, LEFT)
						elif y < 4*square_size:
							print('going right from 6 wraps to the bottom of 3 (right -> up)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 2, UP)
						else:
							raise ValueError(f'Something went wrong wrapping right at nx={nx}')
				elif facing == 2:  # Left <-
					nx = x - 1
					if nx < 0 or input_map[y][nx] == ' ':  # wrap around
						# 14
						# 2
						#53
						#6
						if y < square_size:
							print('going left from 1 wraps to the left of 5 (left -> right)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 0, 2, RIGHT)
						elif y < 2*square_size:
							print('going left from 2 wraps to the top of 5 (left -> down)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 0, 2, DOWN)
						elif y < 3*square_size:
							print('going left from 5 wraps to the left of 1 (left -> right)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 0, RIGHT)
						elif y < 4*square_size:
							print('going left from 6 wraps to the top of 1 (left -> down)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 0, DOWN)
						else:
							raise ValueError(f'Something went wrong wrapping left at nx={nx}')
				elif facing == 1:  # Down v
					ny = y + 1
					if ny >= height or x >= len(input_map[ny]) or input_map[ny][x] == ' ':  # wrap around
						# 14
						# 2
						#53
						#6
						if x < square_size:
							print('going down from 6 wraps to the top of 4 (down -> down)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 2, 0, DOWN)
						elif x < 2*square_size:
							print('going down from 3 wraps to the right of 6 (down -> left)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 0, 3, LEFT)
						elif x < 3*square_size:
							print('going down from 4 wraps to the right of 2 (down -> left)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 1, LEFT)
						else:
							raise ValueError(f'Something went wrong wrapping down from ny={ny}')
				elif facing == 3:  # Up ^
					ny = y-1
					if ny < 0 or x >= len(input_map[ny]) or input_map[ny][x] == ' ':  # wrap around
						# 14
						# 2
						#53
						#6
						if x < square_size:
							print('going up from 5 wraps to the left of 2 (up -> right)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 1, 1, RIGHT)
						elif x < 2*square_size:
							print('going up from 1 wraps to the left of 6 (up -> right)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 0, 3, RIGHT)
						elif x < 3*square_size:
							print('going up from 4 wraps to the bottom of 6 (up -> up)')
							nx, ny, n_facing = edge_wrap(x, y, facing, 0, 3, UP)
						else:
							raise ValueError(f'Something went wrong wrapping up from ny={ny}')
				if input_map[ny][nx] == '#':  # wall, stop
					print(f'Hit wall at [{nx},{ny}]')
					break
				else:  # move to new position and facing
					x, y, facing = nx, ny, n_facing
	print(f'Tile ({x//square_size},{y//square_size}) Offset ({x%square_size},{y%square_size}) Facing {facing}')
	print(x, y, facing)
	return 1000*(y+1) + 4*(x+1) + facing

# print(navigate_cube(sample_map, sample_directions))
print(navigate_cube(input_map, input_directions))  # Not 19317, not 5501, not 43253, not 59396, not 7287
# 52263???
# You begin the path in the leftmost open tile of the top row of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).

# To finish providing the password to this strange input device, you need to determine numbers for your final row, column, and facing as your final position appears from the perspective of the original map.
# Rows start from 1 at the top and count downward; columns start from 1 at the left and count rightward.
# (In the above example, row 1, column 1 refers to the empty space with no tile on it in the top-left corner.)
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^). The final password is the sum of 1000 times the row, 4 times the column, and the facing.

# In the above example, the final row is 6, the final column is 8, and the final facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.
