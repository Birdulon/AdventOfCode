with open('day4-input', 'r') as file:
  data = sorted([l.strip('\n') for l in file])
import numpy as np

GUARDs = {}
GUARD = None
GUARD_asleep = False
GUARD_sleeptime = 0

def parse(line):
  global GUARD, GUARD_asleep, GUARD_sleeptime
  date, time, *event = line.split()
  date = date.lstrip('[')
  time = time.rstrip(']')
  minute = int(time.partition(':')[2])
  if event[0] == 'Guard':
    if GUARD_asleep and GUARD:
      GUARDs[GUARD][GUARD_sleeptime:minute] += 1
    GUARD = int(event[1].lstrip('#'))
    if GUARD not in GUARDs:
      GUARDs[GUARD] = np.zeros((60))
    GUARD_asleep = False
  elif event[0] == 'wakes':
    GUARD_asleep = False
    if GUARD:
      GUARDs[GUARD][GUARD_sleeptime:minute] += 1
  else:  # falls asleep
    GUARD_asleep = True
    GUARD_sleeptime = minute


for line in data:
  parse(line)

max_mins = 0
max_g = None
for k, v in GUARDs.items():
  val = v.sum()
  if val > max_mins:
    max_mins = val
    max_g = k
biggest_minute = GUARDs[max_g].argmax()
print(max_g*biggest_minute)  # Part 1


max_mins_2 = 0
max_g_2 = None
for k, v in GUARDs.items():
  val = v.max()
  if val > max_mins_2:
    max_mins_2 = val
    max_g_2 = k
print(max_g_2*GUARDs[max_g_2].argmax())  # Part 2
