from helpers import *

def run_machine(l):
	x = 1
	cycle = 1
	X = np.ones(len(l)*2, dtype=dtype)
	for line in l:
		ins = line[:4]
		if ins == 'addx':
			cycle += 2
			X[cycle:] += int(line[5:])
		elif ins == 'noop':
			cycle += 1
	X = X[:cycle+1]
	I = np.arange(cycle+1)
	sig_strength = sum((X*I)[(I+20)%40 == 0])
	print(f'Part 1: Signal strength sampled at 20, 60, 100... = {sig_strength}')
	SCREEN_X = I % 40
	SCREEN = np.zeros_like(X)
	SCREEN[abs(SCREEN_X-X-1) <= 1] = 1
	print('Part 2: Display output below')
	for i in range(1, cycle, 40):
		print(''.join(' ' if c==0 else '#' for c in SCREEN[i:i+40]))

run_machine(read_day(10).split('\n'))
