with open('input/3', 'r') as file:
    input = file.read().strip().split('\n')

def prio(character):
    if 'a' <= character <= 'z':
        return ord(character) - ord('a') + 1
    return ord(character) - ord('A') + 27


s = 0
for line in input:
    l = len(line)//2
    left = set(line[:l])
    right = set(line[l:])
    common = left & right
    character = list(common)[0]
    s += prio(character)
print(s)  # Part 1 answer


s = 0
for group in range(len(input)//3):
    e1 = set(input[group*3])
    e2 = set(input[group*3+1])
    e3 = set(input[group*3+2])
    common = e1 & e2 & e3
    character = list(common)[0]
    s += prio(character)
print(s)  # Part 2 answer