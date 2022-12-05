import re
numbers_pattern = re.compile(r'((?:(?<!\d)-)?\d+)')

with open('input/5', 'r') as file:
    input_stacks, _, input_orders = file.read().strip().partition('\n\n')

input_stacks_split = input_stacks.split('\n')
input_stacks_transposed = [''.join(l[i] for l in input_stacks_split[::-1]).strip(' []') for i in range(len(input_stacks_split[0]))]
starting_stack_strings = {int(l[0]):l[1:] for l in input_stacks_transposed if len(l) > 0}
order_numbers = [[int(x) for x in numbers_pattern.findall(line)] for line in input_orders.split('\n')]

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
