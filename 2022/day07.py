with open('input/07', 'r') as file:
	lines = file.read().strip().split('\n')
pwd = []
files = {}

for line in lines:
	# print(pwd, line)
	if line[0] == '$':
		if line[2:4] == 'cd':
			_, _, newdir = line.rpartition(' ')
			if newdir == '/':
				pwd = []
			elif newdir.startswith('/'):
				pwd = newdir[1:].split('/')
			elif newdir == '..':
				pwd.pop()
			else:
				pwd += newdir.split('/')
		elif line[2:4] == 'ls':
			pass
	elif line[:3] == 'dir':
		pass
	else:
		size, _, filename = line.partition(' ')
		l = int(size)
		dir = files
		for d in pwd:
			dir[d] = dir.get(d, {})
			dir = dir[d]
		dir[filename] = l

dir_sizes = {}
def get_dir_size(dir_name, dir):
	if dir_name in dir_sizes:
		return dir_sizes[dir_name]
	s = 0
	for filename, v in dir.items():
		if isinstance(v, dict):
			s += get_dir_size(dir_name + '/' + filename, v)
		else:
			s += v
	dir_sizes[dir_name] = s
	return s
get_dir_size('/', files)

print(f'Part 1: {sum([v for v in dir_sizes.values() if v <= 100000])}')  # 1118405


total_capacity = 70_000_000
need = 30_000_000
remaining_capacity = total_capacity - dir_sizes['/']
target = need - remaining_capacity

print(f'Part 2: {sorted([v for v in dir_sizes.values() if v >= target])[0]}')
