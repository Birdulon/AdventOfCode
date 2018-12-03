with open('day2-input') as file:
  data = file.readlines()
lines = [d.rstrip('\n') for d in data]
twos = 0
threes = 0
for line in lines:
  charcounts = {}
  for c in line:
    if c in charcounts:
      charcounts[c] += 1
    else:
      charcounts[c] = 1
  if 2 in charcounts.values():
    twos += 1
  if 3 in charcounts.values():
    threes += 1
print(twos * threes)  # Part 1

def diff(s1, s2):
  count = 0
  common = []
  for c1, c2 in zip(s1, s2):
    if c1 != c2:
      count += 1
    else:
      common.append(c1)
  return count, common

for i, line in enumerate(lines):
  for line2 in lines[i:]:
    count, common = diff(line, line2)
    if count == 1:
      print(line, line2, ''.join(common))  # Part 2
      break
