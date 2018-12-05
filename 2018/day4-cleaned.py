with open('day4-input', 'r') as file:
  data = sorted([l.strip('\n') for l in file])
import numpy as np

guards = {}
guard = None
guard_sleep = None

for line in data:
  _, time, *event = line.split()
  minute = int(time[-3:-1])
  if event[0] == 'Guard':
    if guard_sleep is not None:
      raise Exception("Last guard didn't wake up?!")
    guard = int(event[1][1:])
    if guard not in guards:
      guards[guard] = np.zeros((60))
  elif event[0] == 'wakes':
    guards[guard][guard_sleep:minute] += 1
    guard_sleep = None
  else:  # falls asleep
    guard_sleep = minute

for func in (np.sum, np.max):  # Part 1, Part 2. Pattern shamelessly copied from Peter Tseng's Ruby solution.
  guard, minutes = max(guards.items(), key=lambda x: func(x[1]))
  print(guard * minutes.argmax())
