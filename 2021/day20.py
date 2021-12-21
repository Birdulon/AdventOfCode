import numpy as np
from sys import argv

filename = argv[1] if len(argv)>1 else 'day20input'

def unfold(func, arg, n):
    for _ in range(n):
        arg = func(arg)
        yield arg


mapping = {'#':1, '.':0}
with open(filename, 'r') as file:
    rawinput = file.read().strip()
    cipher_str, _, input_str = rawinput.partition('\n\n')
    cipher = np.array([mapping[c] for c in cipher_str], dtype=np.int8)
    input_arr = np.array([[mapping[c] for c in string] for string in input_str.split('\n')], dtype=np.int8)

roll_offsets = [(x,y) for y in [1,0,-1] for x in [1,0,-1]]  # Note roll is opposite direction to our sampling  i.e. (1,1) means (0,0) is old (-1,-1)
def sample(array):
    #lookup_values = sum([2**(8-n)*np.roll(array, offset, (1,0)) for n,offset in enumerate(roll_offsets)])  # Note axis 1 is x axis 0 is y.
    lookup_values = np.sum([2**(8-n)*np.roll(array, offset, (1,0)) for n,offset in enumerate(roll_offsets)], 0, dtype=np.int16)  # Note axis 1 is x axis 0 is y.
    return cipher[lookup_values]

def visualize(array):
    print('\n'.join(''.join(['.','#'][c] for c in row) for row in array))


simulated_lights = [t.sum() for t in unfold(sample, np.pad(input_arr, 51), 50)]
print('Part 1: Lights after 2 enhancements:', simulated_lights[2-1])
print('Part 2: Lights after 50 enhancements:', simulated_lights[50-1])
