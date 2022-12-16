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
	for _ in range(len(adjacent_valves)):
		for i, adj in enumerate(adjacent_valves):  # Import routes from adj
			for a in adj:
				for j, p in enumerate(paths[a]):
					if p is None:
						continue
					if paths[i,j] is None or (len(p)+1) < len(paths[i,j]):
						paths[i,j] = p + [i]
	# print(paths)
	path_costs = np.vectorize(len)(paths)
	return path_costs

T_MAX = 30
times_called = np.zeros(T_MAX, dtype=dtype)
def simulate(valves: dict):
	# print(valves)
	v_keys = {k:i for i,k in enumerate(sorted(valves.keys()))}
	# adjacent_valves = {k:v[1] for k,v in valves.items()}
	# flows = {k:v[0] for k,v in valves.items()}
	adjacent_valves = []
	for k in v_keys:
		adj = valves[k][1]
		if isinstance(adj, list):
			adjacent_valves.append([v_keys[a] for a in adj])
		else:
			adjacent_valves.append([v_keys[adj]])
	flows = [valves[k][0] for k in v_keys]
	print(v_keys)
	path_costs = generate_path_costs(adjacent_valves)
	print(path_costs)

	MAX_FLOW = sum(flows)
	MAX_REMAINING = [i*MAX_FLOW for i in range(T_MAX, -1, -1)]

	def sim_step(position, closed_valves, cur_flow=0, vented=0, t=0, max_vented=0) -> int:
		global times_called
		times_called[t] += 1

		t += 1
		# cur_flow = MAX_FLOW - sum((flows[i] for i in closed_valves))
		vented += cur_flow
		if t >= T_MAX:
			# print(f'sim_step finished with {position} {closed_valves}, {vented}, {t}')
			return max(max_vented, vented)
		if (vented + MAX_REMAINING[t]) < max_vented:  # dead tree
			# print(f'sim_step died with {position} {closed_valves}, {vented}, {t}')
			return max_vented

		if position in closed_valves:
			max_vented = sim_step(position, closed_valves - {position}, cur_flow + flows[position], vented, t, max_vented)
		for target_valve in closed_valves:
			tn = min(t + path_costs[position,target_valve], T_MAX-1)
			dt = tn - t - 1
			max_vented = sim_step(target_valve, closed_valves, cur_flow, vented+dt*cur_flow, tn, max_vented)
		if True:  #len(closed_valves) == 0:  # Wait it out
			tn = T_MAX-1
			dt = tn - t - 1
			max_vented = sim_step(position, closed_valves, cur_flow, vented+dt*cur_flow, tn, max_vented)
		return max_vented

	return sim_step(v_keys['AA'], {i for i,flow in enumerate(flows) if flow > 0})

max_pressure_vented = simulate(parse(sample_lines))
print(max_pressure_vented)
max_pressure_vented = simulate(parse(lines))
print(max_pressure_vented)
