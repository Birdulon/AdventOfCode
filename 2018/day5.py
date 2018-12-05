with open('day5-input', 'r') as file:
  data = [l.strip('\n') for l in file]
# import numpy as np
polymer = [c for c in reversed(data[0])]
# polymer = [c for c in 'dabAcCaCBAcCcaDA']

i = 0
print(len(polymer))
while i < len(polymer)-1:
  if polymer[i] == polymer[i+1].swapcase():
    polymer.pop(i)
    polymer.pop(i)
    i -= 2
  i += 1
print(len(polymer))  # Not 11196?!
while i < len(polymer) - 1:
  if polymer[i] == polymer[i + 1].swapcase():
    polymer.pop(i)
    polymer.pop(i)
    i -= 2
  i += 1
print(len(polymer))  # Not 11196?!
while i < len(polymer) - 1:
  if polymer[i] == polymer[i + 1].swapcase():
    polymer.pop(i)
    polymer.pop(i)
    i = -1
  i += 1

print(len(polymer))  # Part 1

remaining_letters = {}
for c in polymer:
  c = c.lower()
  if c in remaining_letters:
    remaining_letters[c] += 1
  else:
    remaining_letters[c] = 1
print(max(remaining_letters.items(), key=lambda x: x[1]))

def react(letter):
  polymer_2 = [c for c in data[0] if c.lower() != letter]
  i = 0
  while i < len(polymer_2)-1:
    if polymer_2[i] == polymer_2[i+1].swapcase():
      polymer_2.pop(i)
      polymer_2.pop(i)
      i -= 2
    i += 1
  while i < len(polymer_2) - 1:
    if polymer_2[i] == polymer_2[i + 1].swapcase():
      polymer_2.pop(i)
      polymer_2.pop(i)
      i = -1
    i += 1
  return len(polymer_2)
# print(len(polymer_2))  # Not 10658?!
removals = [react(i) for i in remaining_letters.keys()]
print(max(removals))  # Part 2
