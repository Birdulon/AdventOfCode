import numpy as np

with open('input/08', 'r') as file:
	lines = file.read().strip().split('\n')
numbers = np.array([[int(x) for x in line] for line in lines])

w, h = numbers.shape
seen_arr = np.zeros_like(numbers)
seen_arr[0,:] = 1
seen_arr[-1,:] = 1
seen_arr[:,0] = 1
seen_arr[:,-1] = 1

for x in range(w):
	highest_seen = numbers[x,0]
	for y in range(1, h):
		n = numbers[x,y]
		if n > highest_seen:
			seen_arr[x,y] = 1
			highest_seen = n
	highest_seen = numbers[x,h-1]
	for y in range(h-2, 0, -1):
		n = numbers[x,y]
		if n > highest_seen:
			seen_arr[x,y] = 1
			highest_seen = n
for y in range(h):
	highest_seen = numbers[0,y]
	for x in range(1, w):
		n = numbers[x,y]
		if n > highest_seen:
			seen_arr[x,y] = 1
			highest_seen = n
	highest_seen = numbers[w-1,y]
	for x in range(w-2, 0, -1):
		n = numbers[x,y]
		if n > highest_seen:
			seen_arr[x,y] = 1
			highest_seen = n
print(f'Part 1: {seen_arr.sum()}')

seen_arr = np.zeros_like(numbers)
for x in range(1,w-1):
	for y in range(1,h-1):
		seen = np.zeros(4, dtype=np.int32)
		treehouse = numbers[x,y]
		for x1 in range(x+1, w):
			seen[0] += 1
			if numbers[x1,y] >= treehouse:
				break
		for x1 in range(x-1, -1, -1):
			seen[1] += 1
			if numbers[x1,y] >= treehouse:
				break
		for y1 in range(y+1, h):
			seen[2] += 1
			if numbers[x,y1] >= treehouse:
				break
		for y1 in range(y-1, -1, -1):
			seen[3] += 1
			if numbers[x,y1] >= treehouse:
				break
		score = seen.prod()
		# print(f'{x},{y}: {seen} = {score}')
		seen_arr[x,y] = score
print(f'Part 2: {seen_arr.max()}')
