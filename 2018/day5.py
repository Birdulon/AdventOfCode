with open('day5-input', 'r') as file:
  data = [l.strip('\n') for l in file]
polymer = [c for c in data[0]]
# polymer = [c for c in 'dabAcCaCBAcCcaDA']

def react(poly):
  i = 0
  while i < len(poly)-1:
    if poly[i] == poly[i+1].swapcase():
      poly.pop(i+1)
      poly.pop(i)
      i = max(i-1, 0)
    else:
      i += 1
  return poly

print(len(react(list(polymer))))  # Part 1

remaining_letters = set(c.lower() for c in polymer)
removals = [len(react([c for c in polymer if c.lower() != i])) for i in remaining_letters]
print(min(removals))  # Part 2
