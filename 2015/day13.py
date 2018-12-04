with open('day13-input', 'r') as file:
  data = [l.strip('\n') for l in file]

from itertools import permutations

guests = set()
points = {}

for line in data:
  guest1, _, sign, point, _, _, _, _, _, _, guest2 = line.rstrip('.').split(' ')
  guests.add(guest1)
  guests.add(guest2)
  mul = -1 if sign == 'lose' else +1
  points[(guest1, guest2)] = mul*int(point)

route_points = []
for route in permutations(guests):
  route_points.append(sum([points[b, a]+points[b, c] for a, b, c in zip(route, route[1:]+route[:1], route[2:]+route[:2])]))
print(max(route_points))  # Part 1

guests.add('Me')
def get_points(guest1, guest2):
  if guest1 == 'Me' or guest2 == 'Me':
    return 0
  else:
    return points[(guest1, guest2)]

route_points_2 = []
for route in permutations(guests):
  route_points_2.append(sum([get_points(b, a)+get_points(b, c) for a, b, c in zip(route, route[1:]+route[:1], route[2:]+route[:2])]))
print(max(route_points_2))  # Part 2
