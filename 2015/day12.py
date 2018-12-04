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

number_sum_2 = 0.0
def count(obj):
  if isinstance(obj, dict):
    if 'red' in obj.values() or 'red' in obj.keys():
      return
    for i in obj.keys():
      count(i)
    for i in obj.values():
      count(i)
  elif isinstance(obj, list):
    for i in obj:
      count(i)
  elif not isinstance(obj, str):
    global number_sum_2
    number_sum_2 += obj

for d in data:
  count(d)
print(number_sum_2)  # Part 2
