from helpers import *
input_stripped = read_day(day)
lines = input_stripped.split('\n')

sample_lines = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''.strip().split('\n')

def make_heightmap(lines: list[str]) -> tuple[ArrayLike, ArrayLike, ArrayLike]:
    heightmap = np.zeros((len(lines[0]), len(lines)), dtype=dtype)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'S':
                heightmap[x,y] = 0
                start = np.array([x,y], dtype=dtype)
            elif c == 'E':
                heightmap[x,y] = 25
                end = np.array([x,y], dtype=dtype)
            else:
                heightmap[x,y] = ord(c) - ord('a')
    return heightmap, start, end

# def make_cell_costs(position, heightmap):
#     init_val = 9_999_999
#     costs = np.full_like(heightmap, init_val)
#     pos_t = tuple(position)
#     costs[pos_t] = 0
#     curr_positions = {pos_t}
#     while (costs == init_val).any() and len(curr_positions) > 0:
#         next_positions = set()
#         for pos_t in curr_positions:
#             n_h_limit = heightmap[pos_t] + 1
#             n_cost = costs[pos_t] + 1
#             for d in directions_array:
#                 next_t = (pos_t[0] + d[0], pos_t[1] + d[1])
#                 if (0 <= next_t[0] < heightmap.shape[0]) and (0 <= next_t[1] < heightmap.shape[1]):
#                     hn = heightmap[next_t]
#                     if n_h_limit >= hn and costs[next_t] > n_cost:
#                         costs[next_t] = n_cost
#                         next_positions.add(next_t)
#         curr_positions = next_positions
#     return costs

def make_reversed_cell_costs(position, heightmap):
    init_val = 9_999_999
    costs = np.full_like(heightmap, init_val)
    pos_t = tuple(position)
    costs[pos_t] = 0
    curr_positions = {pos_t}
    while (costs == init_val).any() and len(curr_positions) > 0:
        next_positions = set()
        for pos_t in curr_positions:
            n_h_limit = heightmap[pos_t] - 1
            n_cost = costs[pos_t] + 1
            for d in directions_array:
                next_t = (pos_t[0] + d[0], pos_t[1] + d[1])
                if (0 <= next_t[0] < heightmap.shape[0]) and (0 <= next_t[1] < heightmap.shape[1]):
                    hn = heightmap[next_t]
                    if n_h_limit <= hn and costs[next_t] > n_cost:
                        costs[next_t] = n_cost
                        next_positions.add(next_t)
        curr_positions = next_positions
    return costs

# heightmap, start, end = make_heightmap(sample_lines)
heightmap, start, end = make_heightmap(lines)
rev_costs = make_reversed_cell_costs(end, heightmap)

start_score = rev_costs[*start]
print(f'Part 1: {start_score}')
start_candidates = {tuple(pos) for pos in np.transpose(np.nonzero(heightmap == 0))}
best_candidate = start
best_score = start_score
for candidate in start_candidates:
    score = rev_costs[*candidate]
    if score < best_score:
        best_candidate = candidate
        best_score = score
print(f'Part 2: start at {best_candidate}: cost of {best_score}')
