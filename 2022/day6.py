with open('input/6', 'r') as file:
    line = file.read().strip()

for i in range(len(line)-3):
    chars = set(line[i:i+4])
    if len(chars) == 4:
        print(f'Part 1: first marker after character {i+4}')
        break

for i in range(len(line)-13):
    chars = set(line[i:i+14])
    if len(chars) == 14:
        print(f'Part 2: first marker after character {i+14}')
        break
