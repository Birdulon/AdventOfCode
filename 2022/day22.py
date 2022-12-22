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

print(navigate(sample_map, sample_directions))
print(navigate(input_map, input_directions))  # Not 132096
# You begin the path in the leftmost open tile of the top row of tiles. Initially, you are facing to the right (from the perspective of how the map is drawn).

# To finish providing the password to this strange input device, you need to determine numbers for your final row, column, and facing as your final position appears from the perspective of the original map.
# Rows start from 1 at the top and count downward; columns start from 1 at the left and count rightward.
# (In the above example, row 1, column 1 refers to the empty space with no tile on it in the top-left corner.)
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^). The final password is the sum of 1000 times the row, 4 times the column, and the facing.

# In the above example, the final row is 6, the final column is 8, and the final facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.
