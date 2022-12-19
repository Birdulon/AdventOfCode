from helpers import *
from multiprocessing import Pool
lines = read_day(19).split('\n')

sample_lines = '''
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''.strip().split('\n')

maximum_potential = np.arange(33, dtype=np.int8).cumsum()

def bp_quality(line, t_max=24):
	bp, cost_orebot_ore, cost_claybot_ore, cost_obsbot_ore, cost_obsbot_clay, cost_geodebot_ore, cost_geodebot_obs = line_to_numbers(line)
	# print(line)
	# Ore, Clay, Obsidian, Geode
	orebot_cost = np.array([cost_orebot_ore, 0, 0], dtype=np.int8)
	claybot_cost = np.array([cost_claybot_ore, 0, 0], dtype=np.int8)
	obsbot_cost = np.array([cost_obsbot_ore, cost_obsbot_clay, 0], dtype=np.int8)
	geodebot_cost = np.array([cost_geodebot_ore, 0, cost_geodebot_obs], dtype=np.int8)
	robot_orders = (  # Special ordering to try and hit best case earliest
		(1, claybot_cost),
		(0, orebot_cost),
		(2, obsbot_cost),
		(None, geodebot_cost),
	)
	max_robots = np.array([max(cost_orebot_ore, cost_claybot_ore, cost_obsbot_ore, cost_geodebot_ore), cost_obsbot_clay, cost_geodebot_obs], dtype=np.int8)

	search_stack = []
	seen = set()
	def add_state(t, robot_counts, res_counts, geodes_total):
		state = (t, tuple(robot_counts), tuple(res_counts), geodes_total)
		if state not in seen:
			search_stack.append((t, robot_counts, res_counts, geodes_total))
			seen.add(state)

	add_state(0, np.array((1,0,0), dtype=np.int8), np.array((0,0,0), dtype=np.int8), 0)
	geodes_best = 0
	while len(search_stack) > 0:
		t, robot_counts, res_counts, geodes_total = search_stack.pop()
		if t < t_max:
			if (geodes_total + maximum_potential[t_max-t]) < geodes_best:
				continue
			for idx, cost in robot_orders:
				if idx is not None:
					if robot_counts[idx] >= max_robots[idx]:
						continue
					next_robots = robot_counts.copy()
					next_robots[idx] += 1
				mask = cost > 0  # Only look at resources within the cost
				if np.any(robot_counts[mask] == 0):  # no robot no income, we can't just wait to build it
					continue
				time_to_resources = max(-(-(cost[mask] - res_counts[mask]) // robot_counts[mask]))
				dt = max(0, time_to_resources) + 1  # Always need one minute to build something after having the resources ready
				nt = t + dt
				if nt < t_max:  # Nothing interesting can happen on the very last minute
					new_res = res_counts + (dt * robot_counts) - cost
					if idx is None:  # Special case for Geodebots
						add_state(nt, robot_counts, new_res, geodes_total+(t_max-nt))
					else:
						add_state(nt, next_robots, new_res, geodes_total)
		geodes_best = max(geodes_best, geodes_total)

	quality = bp * geodes_best
	print(f'Blueprint {bp}: at {t_max} minutes: max geodes {geodes_best}, quality number = {quality}')
	return bp, geodes_best, quality

def bp_quality32(line):
	return bp_quality(line, 32)

if __name__ == '__main__':
	with Pool(8) as p:
		depth32 = p.map_async(bp_quality32, lines[:3])
		depth24 = p.map_async(bp_quality, lines)
		qual_tally = sum((quality for bp, max_geodes, quality in depth24.get()))
		print(f'Part 1: {qual_tally}')
		max_prod = prod((max_geodes for bp, max_geodes, quality in depth32.get()))
		print(f'Part 2: {max_prod}')
	# qual_tally = sum((bp_quality(line)[-1] for line in lines))
	# print(f'Part 1: {qual_tally}')
	# max_prod = prod((max_geodes for bp, max_geodes, quality in map(bp_quality32, lines[:3])))
	# print(f'Part 2: {max_prod}')
