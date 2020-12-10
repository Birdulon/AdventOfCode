import re
ex = re.compile(r'(\d+)-(\d+) (\w): (.*)')
f = lambda i,j,c,s: (int(i), int(j), c, s)  # Wish I could sneak this into the listcomp but can't think of a fun way to do that at present :(
with open('input02', 'r') as file:
  data = [f(*ex.match(line).groups()) for line in file.readlines()]

print(f'Part 1: {[(i<=s.count(c)<=j) for i,j,c,s in data].count(True)}')
print(f'Part 2: {[(s[i-1]==c)^(s[j-1]==c) for i,j,c,s in data].count(True)}')  # This is fragile, beware inputs that may have indices out of range!
