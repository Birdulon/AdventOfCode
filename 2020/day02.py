import re
ex = re.compile(r'(\d+)-(\d+) (\w): (.*)')
with open('input02', 'r') as file:
  data = [ex.match(line).groups() for line in file.readlines()]

valid = [(int(i)<=s.count(c)<=int(j)) for i,j,c,s in data]
print(f'Part 1: {valid.count(True)}')

valid2 = [(s[int(i)-1]==c)^(s[int(j)-1]==c) for i,j,c,s in data]  # This is fragile, beware inputs that may have indices out of range!
print(f'Part 2: {valid2.count(True)}')
