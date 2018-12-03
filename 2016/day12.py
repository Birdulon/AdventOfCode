with open('day12-input', 'r') as file:
  data = [l.strip('\n') for l in file]
TOKENS = [line.split(' ') for line in data]

def run(registers):
  def get(key):
    try:
      return registers[key]
    except KeyError:
      return int(key)
  i = 0
  while i < len(data):
    tokens = TOKENS[i]  # data[i].split(' ')
    if tokens[0] == 'cpy':
      registers[tokens[2]] = get(tokens[1])
    elif tokens[0] == 'inc':
      registers[tokens[1]] += 1
    elif tokens[0] == 'dec':
      registers[tokens[1]] -= 1
    else:  # elif tokens[0] == 'jnz':
      if get(tokens[1]) != 0:
        i += int(tokens[2]) - 1
    i += 1
registers1 = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
run(registers1)
print(registers1['a'])  # Part 1

registers2 = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
run(registers2)
print(registers2['a'])  # Part 2 - Slow!
