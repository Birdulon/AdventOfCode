from helpers import *
lines = read_day(15).split('\n')
sample_lines = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''.strip().split('\n')

def do_sensors(lines: list[str], row: int):
	seen_cells_on_row = set()
	for line in lines:
		x, y, nx, ny = line_to_numbers(line)
		distance = abs(x-nx) + abs(y-ny)
		dr = abs(y-row)
		if dr < distance:
			d2 = distance - dr
			seen_cells_on_row |= {x+i for i in range(-d2, d2+1)}
	print(f'Part 1: {len(seen_cells_on_row) - 1}')
# do_sensors(sample_lines, 20)
do_sensors(lines, 2_000_000)

def in_range_of_sensors(sensors, x, y):
	for (i,j,d) in sensors:
		if abs(x-i) + abs(y-j) <= d:
			d2 = d - abs(x-i)
			y_advance = (j+d2)-y + 1
			return y_advance
	return False

def do_sensors_2(lines: list[str], search_space: int):
	sensors = []
	for num, line in enumerate(lines, 1):
		x, y, nx, ny = line_to_numbers(line)
		if not ((0 <= x <= 4_000_000) and (0 <= y <= 4_000_000)):
			continue
		distance = abs(x-nx) + abs(y-ny)
		sensors.append((x, y, distance))

	# print(sensors)
	for x in range(0, search_space+1):
		# if x % 100_000 == 0:
		# 	print(f'Processed {x} rows')
		y = 0
		while y <= search_space:
			y_skip = in_range_of_sensors(sensors, x, y)
			if y_skip is False:
				print(f'Part 2: Seen at ({x},{y}) = submit {x*4000000 + y}')
				return
			y += y_skip

# do_sensors_2(sample_lines, 20)
do_sensors_2(lines, 4_000_000)

