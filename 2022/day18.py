from helpers import *
from skimage.morphology import flood
coords = [tuple(line_to_numbers(line)) for line in read_day(18).split('\n')]

sample_coords = [tuple(line_to_numbers(line)) for line in '''
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''.strip().split('\n')]

def count_faces(coords: list[tuple[int,int,int]]):
	# print(coords)
	surface_area = 0
	for (x,y,z) in coords:
		if (x+1,y,z) not in coords:
			surface_area += 1
		if (x-1,y,z) not in coords:
			surface_area += 1
		if (x,y+1,z) not in coords:
			surface_area += 1
		if (x,y-1,z) not in coords:
			surface_area += 1
		if (x,y,z+1) not in coords:
			surface_area += 1
		if (x,y,z-1) not in coords:
			surface_area += 1
	return surface_area

print(f'Part 1 (sample): {count_faces(sample_coords)}')
print(f'Part 1: {count_faces(coords)}')

def count_faces_2(coords: list[tuple[int,int,int]]):
	# we pad to ensure the outer edges are fine
	field = np.zeros((25,25,25), dtype=np.int8)
	for (x,y,z) in coords:
		field[x+1,y+1,z+1] = 1
	field[flood(field, (0,0,0), connectivity=1)] = -1

	surface_area = 0
	for (x,y,z) in np.argwhere(field == 1):
		if field[x+1,y,z] == -1:
			surface_area += 1
		if field[x-1,y,z] == -1:
			surface_area += 1
		if field[x,y+1,z] == -1:
			surface_area += 1
		if field[x,y-1,z] == -1:
			surface_area += 1
		if field[x,y,z+1] == -1:
			surface_area += 1
		if field[x,y,z-1] == -1:
			surface_area += 1
	return surface_area


print(f'Part 2 (sample): {count_faces_2(sample_coords)}')
print(f'Part 2: {count_faces_2(coords)}')
