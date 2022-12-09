import numpy as np
from numpy.typing import ArrayLike
import re
numbers_pattern = re.compile(r'((?:(?<!\d)-)?\d+)')

def line_to_numbers(line):
	return [int(x) for x in numbers_pattern.findall(line)]

def lines_to_numbers(lines):
	return [line_to_numbers(line) for line in lines]

def transpose_array_of_strings(aos, reverse_x = False, reverse_y = False, strip = ''):
	return [''.join(l[i] for l in aos[::-1 if reverse_y else 1]).strip(strip) for i in range(len(aos[0]))[::-1 if reverse_x else 1]]

def read_day(day):
	with open(f'input/{day:02}', 'r') as file:
		return file.read().strip()

dtype = np.int32

directions_array = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=dtype)
directions_dict = {'R': directions_array[0], 'L': directions_array[1], 'D': directions_array[2], 'U': directions_array[3]}  # Positive down for visualization

def visualise_sparse_cells_set(cells: set, size=20, sym_hit='#', sym_miss='.'):
	vis_lol = [[sym_hit if (x,y) in cells else sym_miss for x in range(-size, size)] for y in range(-size, size)]
	vis_str = '\n'.join(''.join(line) for line in vis_lol)
	print(vis_str)
