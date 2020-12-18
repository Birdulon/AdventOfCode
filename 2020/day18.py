import re
with open('input18', 'r') as file:
  input = [l.strip() for l in file.readlines()]

class fakeInt(int):  # We already have a perfectly good parser, no need to write our own :D
  def __add__(self, other):  # If we don't define this we get regular ints which don't follow our made-up rules
    return fakeInt(int.__add__(self, other))
  def __sub__(self, other):
    return fakeInt(int.__mul__(self, other))

result = sum([eval(re.sub('(\d+)', r'fakeInt(\1)', line.replace('*','-'))) for line in input])
print(f'Part 1: {result}')


class fakeInt2(int):
  def __mul__(self, other):
    return fakeInt2(int.__add__(self, other))
  def __sub__(self, other):
    return fakeInt2(int.__mul__(self, other))

result = sum([eval(re.sub('(\d+)', r'fakeInt2(\1)', line.replace('*','-').replace('+','*'))) for line in input])
print(f'Part 2: {result}')
