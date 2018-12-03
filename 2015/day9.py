with open('day9-input', 'r') as file:
  data = [l.strip('\n') for l in file]

towns = set()
distances = {}
def get_distance(town1, town2):
  if town2 < town1:
    return distances[(town2, town1)]
  else:
    return distances[(town1, town2)]
def set_distance(town1, town2, value):
  if town2 < town1:
    distances[(town2, town1)] = value
  else:
    distances[(town1, town2)] = value

for line in data:
  town1, _, town2, _, distance = line.split(' ')
  towns.add(town1)
  towns.add(town2)
  set_distance(town1, town2, int(distance))

from itertools import permutations
route_distances = []
for route in permutations(towns):
  route_distances.append(sum([get_distance(a, b) for a, b in zip(route[:-1], route[1:])]))
print(min(route_distances))  # Part 1
print(max(route_distances))  # Part 2
