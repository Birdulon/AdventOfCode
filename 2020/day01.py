with open('input01', 'r') as file:
  data = sorted([int(i) for i in file.readlines()])

def find_pair_sum(total, data):
  for x in data:
    y = total - x
    if y in data:
      return x, y
  return None, None

x, y = find_pair_sum(2020, data)
print(f'Part 1: {x}*{y} = {x*y}')

for idx, x in enumerate(data):
  y, z = find_pair_sum(2020-x, data[idx+1:])
  if y:
    print(f'Part 2: {x}*{y}*{z} = {x*y*z}')
    break
