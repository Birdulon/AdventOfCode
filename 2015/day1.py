with open('day1-input', 'r') as file:
  data = file.readlines()
print(data[0].count('(') - data[0].count(')'))  # Part 1
f = 0
for i, c in enumerate(data[0]):
  if c == '(':
    f += 1
  else:
    f -= 1
  if f < 0:
    print(i+1)  # Part 2
    break
