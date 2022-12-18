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

def count_faces(coords: list[tuple[int,int,int]], count_gaps=True):
	# we pad to ensure the outer edges are fine
	field = np.full((25,25,25), -1 if count_gaps else 0, dtype=np.int8)
	# indices = np.array(coords, dtype=np.int8).T + 1
	# field[*indices] = 1
	for (x,y,z) in coords:
		field[x+1,y+1,z+1] = 1

	if not count_gaps:
		field[flood(field, (0,0,0), connectivity=1)] = -1

	surface_area  = np.logical_and(field[:-1,:,:] == 1, field[ 1:,:,:] == -1).sum()
	surface_area += np.logical_and(field[ 1:,:,:] == 1, field[:-1,:,:] == -1).sum()
	surface_area += np.logical_and(field[:,:-1,:] == 1, field[:, 1:,:] == -1).sum()
	surface_area += np.logical_and(field[:, 1:,:] == 1, field[:,:-1,:] == -1).sum()
	surface_area += np.logical_and(field[:,:,:-1] == 1, field[:,:, 1:] == -1).sum()
	surface_area += np.logical_and(field[:,:, 1:] == 1, field[:,:,:-1] == -1).sum()
	return surface_area

print(f'Part 1 (sample): {count_faces(sample_coords)}')
print(f'Part 1: {count_faces(coords)}')


print(f'Part 2 (sample): {count_faces(sample_coords, False)}')
t0 = perf_counter_ns()
print(f'Part 2: {count_faces(coords, False)}')
t1 = perf_counter_ns()

for i in range(1000):
	count_faces(coords, False)
t2 = perf_counter_ns()
for i in range(10000):
	count_faces(coords, False)
t3 = perf_counter_ns()

print(f'Part 2 x1: {(t1-t0)/1000_000:.3f}ms')
print(f'Part 2 x1000: {(t2-t1)/1000_000:.3f}ms')
print(f'Part 2 x10000: {(t3-t2)/1000_000:.3f}ms')
