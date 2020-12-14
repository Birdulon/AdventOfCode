import numpy as np
with open('input09', 'r') as file:
  input = [int(l.strip()) for l in file.readlines()]
inp = np.array(input)

def find_deviant():
  data = np.tile(inp, [25,1])
  for i in range(25):
    data[i,i+1:] += inp[:-i-1]
  for i,num in enumerate(input[25:], 25):
    if not (data[:, max(0, i-25):i] == num).any():
      return num, i

num, i = find_deviant()
print(f'Part 1: first deviant at {i} - {num}')

def find_sumstreak(number):
  inps = inp.cumsum()
  for i in range(len(input)):
    hits = (inps[i:]-inps[i]) == number
    if hits.any():
      return i+1, i+hits.argmax()+1  # Not entirely sure where the +1 snuck in but w/e

i, j = find_sumstreak(num)
print(f'Part 2: slice {i}:{j} - min+max = {inp[i:j].min()+inp[i:j].max()}')
