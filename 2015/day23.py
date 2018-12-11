with open('day23-input', 'r') as file:
  data = [l.strip('\n') for l in file]

tokens = [line.replace(',', '').split() for line in data]

def run_program(registers):
  i = 0
  while i < len(tokens):
    line = tokens[i]
    if line[0] == 'jmp':
      i += int(line[1])
    elif line[0] == 'jie':
      i += int(line[2]) if registers[line[1]] % 2 == 0 else 1
    elif line[0] == 'jio':
      i += int(line[2]) if registers[line[1]] == 1 else 1
    else:
      i += 1
      if line[0] == 'inc':
        registers[line[1]] += 1
      elif line[0] == 'hlf':
        registers[line[1]] //= 2
      elif line[0] == 'tpl':
        registers[line[1]] *= 3
  return registers

print(run_program({'a': 0, 'b': 0}))  # b is Part 1
print(run_program({'a': 1, 'b': 0}))  # b is Part 2
