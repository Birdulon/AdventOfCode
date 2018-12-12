with open('day12-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
import re

# numbers = np.array([[int(s) for s in re.findall(r'-?\d+', d)] for d in data], dtype=np.int64)
max_gens = 50000000000

initial_state = np.array([0 if s=='.' else 1 for s in data[0].split()[-1]])
rules = [np.array([0 if s=='.' else 1 for s in d.split()[0]]+[0 if s=='.' else 1 for s in d.split()[-1]]) for d in data[2:]]


l = len(initial_state)
state = np.zeros(l*20, dtype=np.int64)
state[l*10:l*11] = initial_state
last_state = state.copy()
pots = np.arange(-l*10, l*10)

for gen in range(max_gens):
  print(''.join(['#' if s else '.' for s in state[l*10-2:l*11+5]]), gen, max_gens-gen)
  for plant in range(2, len(state)-2):
    s = last_state[plant-2:plant+3]
    matched = False
    for rule in rules:
      if np.array_equal(rule[:-1], s):
        state[plant] = rule[-1]
        # print('Matched!', rule)
        matched = True
        break
    if not matched:
      state[plant] = 0
  last_state[:] = state[:]

print(pots[state > 0].sum())
