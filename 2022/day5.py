from helpers import *

with open('input/5', 'r') as file:
    input_stacks, _, input_orders = file.read().strip().partition('\n\n')

starting_stack_strings = {int(l[0]):l[1:] for l in transpose_array_of_strings(input_stacks.split('\n'), reverse_y=True, strip=' []') if len(l) > 0}
order_numbers = lines_to_numbers(input_orders.split('\n'))

stacks = {k:[c for c in v] for k,v in starting_stack_strings.items()}
for (num, source, dest) in order_numbers:
    for i in range(num):
        stacks[dest].append(stacks[source].pop())
print('Part 1: ' + ''.join(s[-1] for s in stacks.values()))

stacks = {k:[c for c in v] for k,v in starting_stack_strings.items()}
for (num, source, dest) in order_numbers:
    stacks[dest] += stacks[source][-num:]
    stacks[source] = stacks[source][:-num]
print('Part 2: ' + ''.join(s[-1] for s in stacks.values()))
