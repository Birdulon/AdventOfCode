import logging
# logging.basicConfig(level=logging.DEBUG)
with open('day7-input', 'r') as file:
  data = [l.strip('\n') for l in file]

steps = set()
step_deps = {}
for line in data:
  tokens = line.split()
  step1, step2 = tokens[1], tokens[-3]
  steps.update((step1, step2))
  step_deps[step2] = step_deps.get(step2, []) + [step1]


def assemble_sleigh(all_steps, step_dependencies, workers):
  unprocessed_steps = all_steps.copy()
  ready_steps = set()
  constructing_steps = {}
  completed_steps = set()
  output = []

  time = -1
  while unprocessed_steps:
    time += 1
    for k in list(constructing_steps):
      constructing_steps[k] -= 1
      if constructing_steps[k] < 1:
        completed_steps.add(k)
        output.append(k)
        logging.debug(f'{time:04}: Step {k} complete!')
        constructing_steps.pop(k)

    free_workers = workers - len(constructing_steps)
    if free_workers < 1:
      continue

    for step in unprocessed_steps - ready_steps:
      dependencies = [d for d in step_dependencies.pop(step, []) if d not in completed_steps]
      if dependencies:
        step_dependencies[step] = dependencies
      else:
        ready_steps.add(step)

    for step in list(sorted(ready_steps))[:free_workers]:
      constructing_steps[step] = 60 + ord(step) - 64  # ord('A') is 65
      logging.debug(f'{time:04}: Starting step {step}! ({constructing_steps[step]} seconds remain)')
      unprocessed_steps.remove(step)
      ready_steps.remove(step)

  output += [step for step, time in sorted(constructing_steps.items(), key=lambda x: x[1])]
  time += max(constructing_steps.values())
  return ''.join(output), time


print('Solo - Order {}, completion time {:4d}s'.format(*assemble_sleigh(steps, step_deps.copy(), 1)))  # Part 1, answer is order.
print('5man - Order {}, completion time {:4d}s'.format(*assemble_sleigh(steps, step_deps.copy(), 5)))  # Part 2, answer is time.
