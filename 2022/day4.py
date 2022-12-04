import re
pattern = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

with open('input/4', 'r') as file:
    lines = file.readlines()

count = 0
for group in lines:
    x1, y1, x2, y2 = (int(x) for x in pattern.findall(group)[0])
    if (x2 >= x1) and (y2 <= y1):  # Elf2 inside Elf1
        count += 1
        continue
    if (x2 <= x1) and (y2 >= y1):  # Elf1 inside Elf2
        count += 1
        continue
print(count)  # Part 1

count = 0
for group in lines:
    x1, y1, x2, y2 = (int(x) for x in pattern.findall(group)[0])
    if (x2 >= x1) and (y2 <= y1):  # Elf2 inside Elf1
        count += 1
        continue
    if (x2 <= x1) and (y2 >= y1):  # Elf1 inside Elf2
        count += 1
        continue
    if (x1 <= x2 <= y1) or (x1 <= y2 <= y1):  # Partial overlap
        count += 1
        continue
print(count)  # Part 2
