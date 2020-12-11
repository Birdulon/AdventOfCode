with open('input06', 'r') as file:
  groups = [[set(s) for s in g.split('\n')] for g in file.read().strip().split('\n\n')]
print(f'Part 1: {sum(len(set.union(*g)) for g in groups)}')
print(f'Part 2: {sum(len(set.intersection(*g)) for g in groups)}')
