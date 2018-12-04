with open('day14-input', 'r') as file:
  data = [l.strip('\n') for l in file]

def deer(line):
  name, _, _, speed, _, _, time, _, _, _, _, _, _, rest, _ = line.split()
  return name, (int(speed), int(time), int(rest))

deers = {k:v for k, v in [deer(line) for line in data]}
def avg_speed(speed, time, rest):
  return (speed*time)/(time+rest)
def distance(t, speed, time, rest):
  period = time + rest
  periods, remainder = divmod(t, period)
  distance = periods * speed * time
  distance += min(time, remainder) * speed
  return distance

print(max([distance(2503, *d) for d in deers.values()]))  # Part 1

deerpoints = [0 for k in deers.keys()]
deerstats = [d for d in deers.values()]
for t in range(1, 2504):
  deer_ds = [distance(t, *d) for d in deerstats]
  lead_d = max(deer_ds)
  for i, d in enumerate(deer_ds):
    if d == lead_d:
      deerpoints[i] += 1
print(max(deerpoints))  # Part 2
