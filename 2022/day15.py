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


def do_sensors_2(lines: list[str], search_space: int):
	sensors = []
	for line in lines:
		x, y, nx, ny = line_to_numbers(line)
		distance = abs(x-nx) + abs(y-ny)
		sensors.append((x, y, distance))
	sensors.sort(key=lambda x: x[2])  # smallest distance first

	def in_range_of_sensors(x: int, y: int) -> bool:
		if not (0 <= x <= search_space and 0 <= y <= search_space):
			return True
		for (i,j,d) in sensors:
			if abs(x-i) + abs(y-j) <= d:
				return True
		print(f'Part 2: Seen at ({x},{y}) = submit {x*4_000_000 + y}')
		return False

	# print(sensors)
	for x0, y0, d in sensors:  # Iterate around perimeters
		# print(x0, y0, d)
		y_up = y0 + d + 1
		y_down = y0 - d - 1
		for i in range(d+1):
			for x in (x0+i, x0-i):
				for y in (y_down+i, y_up-i):
					if not in_range_of_sensors(x, y):
						return

# do_sensors_2(sample_lines, 20)
do_sensors_2(lines, 4_000_000)

