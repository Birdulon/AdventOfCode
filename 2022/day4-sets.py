from helpers import *

with open('input/4', 'r') as file:
    sets_per_line = [
        (set(range(min(n[0], n[1]), max(n[0], n[1])+1)),
         set(range(min(n[2], n[3]), max(n[2], n[3])+1)))
        for n in lines_to_numbers(file.readlines())
    ]

count = sum((set1 <= set2 or set1 >= set2) for (set1, set2) in sets_per_line)
print(f'Part 1: {count} elves have no unique work in their pairing')  # Part 1

count = sum((len(set1 & set2) > 0) for (set1, set2) in sets_per_line)
print(f'Part 2: {count} elf pairs have overlapping work in their pairing')  # Part 2
