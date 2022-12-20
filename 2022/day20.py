from helpers import *
from collections import deque
lines = read_day(20).split('\n')
sample_lines = '''
1
2
-3
3
-2
0
4
'''.strip().split('\n')


def mix(numbers: list[int], n=1):
	N = len(numbers)
	mix_order = numbers
	queue = deque(((i, x) for i,x in enumerate(numbers)))  # mix_id, value
	for mix_pass in range(n):
		mixed_count = 0
		while mixed_count < N:
			v = queue.popleft()
			mix_id, value = v
			if mix_id == mixed_count:
				queue.insert(value % (N-1), v)
				mixed_count += 1
			else:
				queue.append(v)
	return [v for i,v in queue]

def get_coords(numbers: list[int]) -> tuple[int,int,int]:
	N = len(numbers)
	i = numbers.index(0)
	return (numbers[(i+1000)%N], numbers[(i+2000)%N], numbers[(i+3000)%N])

def p1(lines: list[str]) -> str:
	numbers = [int(x) for x in lines]
	coords = get_coords(mix(numbers))
	return f'coords: {coords} have sum {sum(coords)}'

def p2(lines: list[str]) -> str:
	numbers = [int(x)*811589153 for x in lines]
	coords = get_coords(mix(numbers, 10))
	return f'coords: {coords} have sum {sum(coords)}'

print(f'Part 1 (sample): {p1(sample_lines)}')
print(f'Part 1: {p1(lines)}')
print(f'Part 2 (sample): {p2(sample_lines)}')
print(f'Part 2: {p2(lines)}')
