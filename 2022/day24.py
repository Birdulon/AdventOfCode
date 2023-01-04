from helpers import *
lines = read_day(24).split('\n')[1:-1]  # strip walls
sample_lines = '''
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''.strip().split('\n')[1:-1]

def sim(lines):
	height = len(lines)
	width = len(lines[0]) - 2
	blizzards_left = set()
	blizzards_right = set()
	blizzards_up = set()
	blizzards_down = set()
	for row, line in enumerate(lines):
		for col, c in enumerate(line[1:-1]):  # strip walls
			if c == '<':
				blizzards_left.add((col, row))
			elif c == '>':
				blizzards_right.add((col, row))
			elif c == '^':
				blizzards_up.add((col, row))
			elif c == 'v':
				blizzards_down.add((col, row))

	def position_free(col: int, row: int, time: int) -> bool:
		if ((col+time)%width, row) in blizzards_left:
			return False
		if ((col-time)%width, row) in blizzards_right:
			return False
		if (col, (row+time)%height) in blizzards_up:
			return False
		if (col, (row-time)%height) in blizzards_down:
			return False
		return True

	seen_states = set()
	state_stack = [(0,-1,0)]
	def try_add_state(col: int, row: int, time: int):
		if col < 0 or col >= width or row < -1 or row >= height:
			return
		if row == -1 and col != 0:
			return
		if not position_free(col, row, time):
			return
		triple = (col, row, time)
		if triple not in seen_states:
			seen_states.add(triple)
			state_stack.append(triple)

	best_time = None
	goal = (width-1, height)

	while state_stack:
		col, row, t = state_stack.pop()
		t1 = t + 1
		goal_distance = goal[0]-col + goal[1]-row  # Manhattan distance
		if goal_distance == 1:  # we're right next to the goal! move there and end this trail
			if best_time:
				best_time = min(best_time, t1)
			else:
				best_time = t1
			continue
		if best_time and (t + goal_distance > best_time):
			continue
		try_add_state(col, row, t1)
		try_add_state(col-1, row, t1)
		try_add_state(col, row-1, t1)
		try_add_state(col+1, row, t1)
		try_add_state(col, row+1, t1)

	return best_time

print(sim(sample_lines))
print(sim(lines))
