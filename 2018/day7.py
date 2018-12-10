with open('day7-input', 'r') as file:
  data = [l.strip('\n') for l in file]

steps = set()
step_deps = {}
for line in data:
  s = line.split()
  step1 = s[1]
  step2 = s[-3]
  steps.add(step1)
  steps.add(step2)
  if step2 in step_deps:
    step_deps[step2] += step1
  else:
    step_deps[step2] = [step1]

queue = [step for step in steps]
step_deps_1 = step_deps.copy()
completed_steps = set()
ready_steps = set()
output = []
while queue:
  for step in queue:
    if step not in step_deps_1:
      ready_steps.add(step)
    else:
      deps = [d for d in step_deps_1[step] if d not in completed_steps]
      if len(deps) > 0:
        step_deps_1[step] = deps
      else:
        ready_steps.add(step)
        step_deps_1.pop(step)
  for step in sorted(ready_steps)[:1]:
    completed_steps.add(step)
    output += step
    queue.remove(step)
    break
  ready_steps = set()
print(''.join(output))  # Part 1

unprocessed_steps = steps.copy()
step_deps_2 = step_deps.copy()
completed_steps_2 = set()
ready_steps_2 = set()
waiting_steps = {}
time = 0
while unprocessed_steps:
  for k in list(waiting_steps.keys()):
    waiting_steps[k] -= 1
    if waiting_steps[k] < 1:
      completed_steps_2.add(k)
      print(f'{time:04}: Step {k} complete!')  # Debug
      waiting_steps.pop(k)
  for step in unprocessed_steps-ready_steps_2:
    if step not in step_deps_2:
      ready_steps_2.add(step)
    else:
      deps = [d for d in step_deps_2[step] if d not in completed_steps_2]
      if len(deps) > 0:
        step_deps_2[step] = deps
      else:
        ready_steps_2.add(step)
        step_deps_2.pop(step)
  for step in list(sorted(ready_steps_2)):
    if len(waiting_steps) >= 5:  # Only 5 workers
      break
    waiting_steps[step] = 60 + ord(step)-64
    print(f'{time:04}: Starting step {step}! ({waiting_steps[step]} seconds remain)')  # Debug
    unprocessed_steps.remove(step)
    ready_steps_2.remove(step)
  time += 1
time += max(waiting_steps.values()) - 1  # t got moved forward 1 at end of while loop
print(time)  # Part 2
