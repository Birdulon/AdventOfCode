import re
numbers_pattern = re.compile(r'((?:(?<!\d)-)?\d+)')

def line_to_numbers(line):
    return [int(x) for x in numbers_pattern.findall(line)]

def lines_to_numbers(lines):
    return [line_to_numbers(line) for line in lines]

def transpose_array_of_strings(aos, reverse_x = False, reverse_y = False, strip = ''):
    return [''.join(l[i] for l in aos[::-1 if reverse_y else 1]).strip(strip) for i in range(len(aos[0]))[::-1 if reverse_x else 1]]
