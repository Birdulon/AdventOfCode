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

def p1(lines: list[str]) -> str:
	N = len(lines)
	numbers = [int(x) for x in lines]
	final_queue = mix(numbers)
	i = final_queue.index(0)
	values = (final_queue[(i+1000)%N], final_queue[(i+2000)%N], final_queue[(i+3000)%N])
	return f'coords: {values} have sum {sum(values)}'

def p2(lines: list[str]) -> str:
	N = len(lines)
	numbers = [int(x)*811589153 for x in lines]
	final_queue = mix(numbers, 10)
	i = final_queue.index(0)
	values = (final_queue[(i+1000)%N], final_queue[(i+2000)%N], final_queue[(i+3000)%N])
	return f'coords: {values} have sum {sum(values)}'

print(f'Part 1 (sample): {p1(sample_lines)}')
print(f'Part 1: {p1(lines)}')
print(f'Part 2 (sample): {p2(sample_lines)}')
print(f'Part 2: {p2(lines)}')
