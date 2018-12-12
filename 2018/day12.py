with open('day12-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np

initial_state = np.array([False if s=='.' else True for s in data[0].split()[-1]], dtype=np.bool)
rules_list = [(sum([0 if s=='.' else 2**i for i, s in enumerate(d.split()[0])]), False if d.split()[-1] == '.' else True)
              for d in data[2:]]
rules = np.array([v for k, v in sorted(rules_list)], dtype=np.bool)
r_transform = np.array([1, 2, 4, 8, 16], dtype=np.int64)
state = set(*initial_state.nonzero())


def perform_generation(input_state):
  working_state = set()
  adj = np.array([-2, -1, 0, 1, 2], dtype=np.int64)
  check_set = {i+j for i in input_state for j in adj}
  for pot in check_set:
    if rules[(r_transform * [p in input_state for p in pot+adj]).sum()]:
      working_state.add(pot)
  return working_state


for gen in range(20):
  state = perform_generation(state)
val = sum(state)
print(val)  # Part 1

state_2 = state.copy()
last_val = val
last_deltas = [None, None, None, None]
LAST_GEN = 50000000000
for gen in range(20, LAST_GEN):
  if gen % 20 == 0:
    val = sum(state_2)
    last_deltas.append(val-last_val)
    last_val = val
    if len(set(last_deltas)) == 1:  # If all the last few deltas are identical, give up
      print(val + (last_deltas[0]*(LAST_GEN-gen)//20))  # Part 2
      break
    last_deltas.pop(0)
  state_2 = perform_generation(state_2)
