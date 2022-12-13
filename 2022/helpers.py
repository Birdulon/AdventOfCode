from numpy.typing import ArrayLike
import numpy as np
from functools import cmp_to_key
from math import prod
import re
import requests
import sys
sys.setrecursionlimit(100000)

try:
	import datetime
	today = datetime.date.today()
	day = today.day
	year = today.year

	import browser_cookie3
	def download_input(day: int = day):
		filename = f'input/{day:02}'
		r = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=browser_cookie3.firefox())
		if r.status_code != 200:
			print(r)
		else:
			with open(filename,'w') as f:
				f.write(r.text)
except ModuleNotFoundError as mod:
	print(f'{mod.args[0]}, automatic input fetching will not work.')

numbers_pattern = re.compile(r'((?:(?<!\d)-)?\d+)')

def line_to_numbers(line: str) -> list[int]:
	return [int(x) for x in numbers_pattern.findall(line)]

def lines_to_numbers(lines: list[str]) -> list[list[int]]:
	return [line_to_numbers(line) for line in lines]

def transpose_array_of_strings(aos: list[str], reverse_x = False, reverse_y = False, strip = '') -> list[str]:
	return [''.join(l[i] for l in aos[::-1 if reverse_y else 1]).strip(strip) for i in range(len(aos[0]))[::-1 if reverse_x else 1]]

def read_day(day: int) -> str:
	with open(f'input/{day:02}', 'r') as file:
		return file.read().strip()

dtype = np.int32
directions_array = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=dtype)
directions_dict = {'R': directions_array[0], 'L': directions_array[1], 'D': directions_array[2], 'U': directions_array[3]}  # Positive down for visualization

def visualise_sparse_cells_set(cells: set[tuple[int, int]], size=20, sym_hit='#', sym_miss='.'):
	vis_lol = [[sym_hit if (x,y) in cells else sym_miss for x in range(-size, size)] for y in range(-size, size)]
	vis_str = '\n'.join(''.join(line) for line in vis_lol)
	print(vis_str)
