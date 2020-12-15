def play_game(data, until):
  last_indices = {v:i for i,v in enumerate(data[:-1])}
  last = data[-1]
  for i in range(len(data), until):
    if last in last_indices:
      n = i-last_indices[last]-1
      last_indices[last] = i-1
      last = n
    else:
      last_indices[last] = i-1
      last = 0
  return last

input = [int(i) for i in '10,16,6,0,1,17'.split(',')]

print(f'Part 1: 2020th number is {play_game(input, 2020)}')
print(f'Part 2: 30000000th number is {play_game(input, 30000000)}')
