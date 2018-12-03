with open('day1-input', 'r') as file:
  data = file.readlines()
nums = [int(d.rstrip('\n')) for d in data]
print(sum(nums))  # Part 1 answer

from itertools import cycle
iterator = cycle(nums)
while(True):
  f += next(iterator)
  if f in freqs:
    print(f)  # Part 2 answer
    break
  freqs.add(f)
