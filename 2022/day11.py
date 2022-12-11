from helpers import *
from math import prod, lcm

input_stripped = read_day(day)
monkeys_input = [m.split('\n') for m in input_stripped.split('\n\n')]
# monkeys_input = [[l.strip() for l in m.split('\n')] for m in input_stripped.split('\n\n')]
num_regex = re.compile(r'(\d+)')
op_regex = re.compile(r'Operation: (new = .*)')

def generate_monkeys(split_input):
    monkeys = {}
    for monkey in monkeys_input:
        m = {
            'id': int(num_regex.findall(monkey[0])[0]),
            'items': [int(x) for x in num_regex.findall(monkey[1])],
            'operation': op_regex.findall(monkey[2])[0],
            'test_divisor': int(num_regex.findall(monkey[3])[0]),
            'true_monkey': int(num_regex.findall(monkey[4])[0]),
            'false_monkey': int(num_regex.findall(monkey[5])[0]),
            'inspections': 0,
        }
        monkeys[m['id']] = m
    return monkeys

def calculate_monkey_business(monkeys):
    inspections = [m['inspections'] for m in monkeys.values()]
    print(inspections)
    return prod(sorted(inspections)[-2:])

# Part 1
monkeys = generate_monkeys(monkeys_input)
for round in range(20):
    for monkey in monkeys.values():
        for item in monkey['items']:
            worry = item
            old = worry
            new = 0
            exec(monkey['operation'])
            worry = new // 3
            if worry % monkey['test_divisor'] == 0:
                monkeys[monkey['true_monkey']]['items'].append(worry)
            else:
                monkeys[monkey['false_monkey']]['items'].append(worry)
            monkey['inspections'] += 1
        monkey['items'] = []
print(f'Part 1: {calculate_monkey_business(monkeys)}')

# Part 2
monkeys = generate_monkeys(monkeys_input)
# divisor = prod([m['test_divisor'] for m in monkeys.values()])
divisor = lcm(*[m['test_divisor'] for m in monkeys.values()])
print(f'Using modular arithmetic of base: {divisor}')

for round in range(10000):
    for monkey in monkeys.values():
        for item in monkey['items']:
            worry = item
            old = worry
            new = 0
            exec(monkey['operation'])
            worry = new % divisor
            if worry % monkey['test_divisor'] == 0:
                monkeys[monkey['true_monkey']]['items'].append(worry)
            else:
                monkeys[monkey['false_monkey']]['items'].append(worry)
            monkey['inspections'] += 1
        monkey['items'] = []
print(f'Part 2: {calculate_monkey_business(monkeys)}')
