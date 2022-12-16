from helpers import *
lines = read_day(day).split('\n')
sample_lines = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''.strip().split('\n')
r = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)')


def parse(lines):
	valves = {}
	for line in lines:
		for match in r.findall(line):
			valve, flow, connections = match
			valves[valve] = (int(flow), connections.split(', '))
	return(valves)


def generate_path_costs(adjacent_valves: list[list]):
	paths = np.full((len(adjacent_valves), len(adjacent_valves)), None, dtype=object)
	for i, adj in enumerate(adjacent_valves):
		paths[i,i] = []
		for a in adj:
			paths[i,a] = [a]
	for _ in range(len(adjacent_valves)):  # Ensure full propagation
		for i, adj in enumerate(adjacent_valves):  # Import routes from adj
			for a in adj:
				for j, p in enumerate(paths[a]):
					if p is None:
						continue
					if paths[i,j] is None or (len(p)+1) < len(paths[i,j]):
						paths[i,j] = p + [i]
	return np.vectorize(len)(paths)


def simulate(valves: dict, num_actors, t_max):
	v_keys = {k:i for i,k in enumerate(sorted(valves.keys()))}
	START = v_keys['AA']
	adjacent_valves = []
	for k in v_keys:
		adj = valves[k][1]
		if isinstance(adj, list):
			adjacent_valves.append([v_keys[a] for a in adj])
		else:
			adjacent_valves.append([v_keys[adj]])
	flows = [valves[k][0] for k in v_keys]
	valve_open_costs = generate_path_costs(adjacent_valves) + 1
	# print(v_keys)
	# print(valve_open_costs)

	def open_valve(valve: int, t: int) -> int:
		return flows[valve] * (t_max - t)

	# Actor: (time, position)
	def sim_step(actors: tuple[tuple[int,int]], closed_valves: set[int], t=0, vented=0, max_vented=0) -> int:
		actors = sorted(actors)  # Sorts by time ascending
		a_t, a_pos = actors[0]
		# If the second one is also ready to act, it goes next in its own call
		for n_pos in closed_valves:
			# Teleport A to next valve, pass time as if we walked there, and open it at that time
			n_a_t = t + valve_open_costs[a_pos,n_pos]
			if n_a_t < t_max:
				n_vented = vented + open_valve(n_pos, n_a_t)
				n_closed = closed_valves - {n_pos}
				n_actors = ((n_a_t, n_pos), *actors[1:])
				n_t = min(a[0] for a in n_actors)  # Run the simulation again at the time when the next actor is ready (may be the same one as this!)
				max_vented = sim_step(n_actors, n_closed, n_t, n_vented, max_vented)
		return max(vented, max_vented)
	default_closed = {i for i,flow in enumerate(flows) if flow > 0}
	return sim_step(((0,START),) * num_actors, default_closed)

print(f'Part 1 example: {simulate(parse(sample_lines), 1, 30)}')
print(f'Part 1: {simulate(parse(lines), 1, 30)}')

print(f'Part 2 example: {simulate(parse(sample_lines), 2, 26)}')
print(f'Part 2: {simulate(parse(lines), 2, 26)}')
