with open('day17-input', 'r') as file:
  data = [int(l.strip('\n')) for l in file]
from itertools import combinations

solutions = 0
solution_sets = []
for n in range(1, len(data)):
  for c in combinations(data, n):
    if sum(c) == 150:
      solutions += 1
      solution_sets.append(c)
print(solutions)  # Part 1

min_containers = min([len(c) for c in solution_sets])
min_c_solutions = 0
for c in solution_sets:
  if len(c) == min_containers:
    min_c_solutions += 1
print(min_c_solutions)  # Part 2