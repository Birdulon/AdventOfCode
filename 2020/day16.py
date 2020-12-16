with open('input16', 'r') as file:
  input = [ls.strip().split('\n') for ls in file.read().strip().split('\n\n')]

import re
fieldregex = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')
ex_fields = lambda x: (x[0], [int(i) for i in x[1:]])

fields = dict(ex_fields(fieldregex.match(line).groups()) for line in input[0])
my_ticket = [int(x) for x in input[1][1].split(',')]
nearby_tickets = [[int(x) for x in line.split(',')] for line in input[2][1:]]

fieldfuncs = {k:(lambda x, v=v: (v[0]<=x<=v[1]) or (v[2]<=x<=v[3])) for k,v in fields.items()}
any_valid = lambda x: any([f(x) for f in fieldfuncs.values()])

print(f'Part 1: error sum = {sum([sum([x for x in ticket if not any_valid(x)]) for ticket in nearby_tickets])}')

valid_tickets = [ticket for ticket in nearby_tickets if all([any_valid(x) for x in ticket])]

confirmed_fields = {}
potential_fields = {i:set(fields.keys()) for i in range(len(fields))}
def sweep():
  for ticket in valid_tickets:
    for i,keys in list(potential_fields.items()):  # We mutate the dict as we iterate
      for key in list(keys):  # We mutate the set as we iterate
        if i in potential_fields:
          if not fieldfuncs[key](ticket[i]):
            potential_fields[i].remove(key)
          if len(potential_fields[i]) == 1:
            c_key = potential_fields.pop(i).pop()
            confirmed_fields[c_key] = i
            for vset in potential_fields.values():
              vset.remove(c_key)

while len(potential_fields) > 0:
  sweep()

from math import prod  # lmao
print(f'Part 2: {prod([my_ticket[i] for key,i in confirmed_fields.items() if key.startswith("departure")])}')
