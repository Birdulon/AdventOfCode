import numpy as np

with open('day18-input', 'r') as file:
	lines = file.read().strip().split('\n')

initial_state = np.array([[1 if c == '#' else 0 for c in line] for line in lines], dtype=np.uint8)

def sim_step(state):
	adjacent_on = np.zeros_like(initial_state, dtype=np.uint8)
	adjacent_on[:-1,:] += state[1:,:]  # Right neighbour
	adjacent_on[1:,:] += state[:-1,:]  # Left neighbour
	adjacent_on[:,:-1] += state[:,1:]  # Down
	adjacent_on[:,1:] += state[:,:-1]  # Up
	adjacent_on[:-1,1:] += state[1:,:-1]  # Up-right
	adjacent_on[1:,1:] += state[:-1,:-1]  # Up-left
	adjacent_on[:-1,:-1] += state[1:,1:]  # Down-right
	adjacent_on[1:,:-1] += state[:-1,1:]  # Down-left
	output = np.zeros_like(state)
	output[state>0] = (adjacent_on[state>0] == 2)
	output[state>0] |= (adjacent_on[state>0] == 3)
	output[state==0] = (adjacent_on[state==0] == 3)
	return output

state = initial_state
for i in range(100):
	state = sim_step(state)
print(f'Part 1: {state.sum()} lights are on after 100 steps')

def set_corners(state):
	state[0,0] = 1
	state[-1,0] = 1
	state[0,-1] = 1
	state[-1,-1] = 1

state = np.copy(initial_state)
set_corners(state)
for i in range(100):
	state = sim_step(state)
	set_corners(state)
print(f'Part 2: {state.sum()} lights are on after 100 steps with locked corners')
