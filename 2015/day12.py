import json
number_sum = 0.0
def parse_int(val):
  i = int(val)
  global number_sum
  number_sum += i
  return i
def parse_float(val):
  i = float(val)
  global number_sum
  number_sum += i
  return i
with open('day12-input', 'r') as file:
  data = json.load(file, parse_float=parse_float, parse_int=parse_int)
print(number_sum)  # Part 1
