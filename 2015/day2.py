with open('day2-input', 'r') as file:
  data = [l.strip('\n') for l in file]
dimensions = [[int(x) for x in d.split('x')] for d in data]

def area(l, w, h):
  sides = [l*w, w*h, h*l]
  slack = min(sides)
  return 2*sum(sides) + slack

print(sum([area(*present) for present in dimensions]))  # Part 1

def ribbon(l, w, h):
  perimeter = 2 * (sum([l,w,h])-max([l,w,h]))
  volume = l*w*h
  return perimeter + volume

print(sum([ribbon(*present) for present in dimensions]))  # Part 2
