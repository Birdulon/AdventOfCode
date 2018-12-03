with open('day3-input', 'r') as file:
  data = file.readlines()

x = 0
y = 0
houses = set()
houses.add((x, y))
for c in data[0]:
  if c == '>':
    x += 1
  elif c == '<':
    x -= 1
  elif c == '^':
    y += 1
  elif c == 'v':
    y -= 1
  houses.add((x, y))
print(len(houses))  # Part 1

x1 = 0
y1 = 0
x2 = 0
y2 = 0
houses2 = set()
houses2.add((0, 0))
for i, c in enumerate(data[0]):
  if i%2:
    if c == '>':
      x1 += 1
    elif c == '<':
      x1 -= 1
    elif c == '^':
      y1 += 1
    elif c == 'v':
      y1 -= 1
    houses2.add((x1, y1))
  else:
    if c == '>':
      x2 += 1
    elif c == '<':
      x2 -= 1
    elif c == '^':
      y2 += 1
    elif c == 'v':
      y2 -= 1
    houses2.add((x2, y2))
print(len(houses2))  # Part 2
