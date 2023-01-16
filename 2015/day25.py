import re

with open('day25-input', 'r') as file:
	line = file.read().strip()
r, c = [int(x) for x in re.findall('row (\d+).*column (\d+)', line)[0]]
print(r, c)

starting_value = 20151125

def get_value(index: int) -> int:
	value = starting_value
	for _ in range(1, index):
		value = (value * 252533) % 33554393
	return value

def fib(x: int) -> int:
	value = 1
	for i in range(1, x):
		value += i
	return value

def get_value_rc(row: int, column: int) -> int:
	stripe_row = row + column - 1
	stripe_row_idx = fib(stripe_row)
	return get_value(stripe_row_idx + column - 1)

print(f'Test: value at row 6, column 6 is {get_value_rc(6, 6)}')
print(f'Part 1: value at row {r}, column {c} is {get_value_rc(r, c)}')
