input = 825401
input_l = [int(c) for c in str(input)]
len_input = len(input_l)

scoreboard = [3, 7]
elf_1 = 0
elf_2 = 1


def do_round():
  global scoreboard, elf_1, elf_2
  e1 = scoreboard[elf_1]
  e2 = scoreboard[elf_2]
  s = e1 + e2
  scoreboard += [int(c) for c in str(s)]
  elf_1 = (elf_1 + 1 + e1) % len(scoreboard)
  elf_2 = (elf_2 + 1 + e2) % len(scoreboard)


while len(scoreboard) < input+10:
  do_round()

print(''.join([str(i) for i in scoreboard[input:input+10]]))  # Part 1

while True:
  do_round()
  if scoreboard[-len_input:] == input_l:
    print(len(scoreboard)-len_input)  # Part 2
    break
  if scoreboard[-len_input-1:-1] == input_l:  # Each round adds 1-2 recipes to end
    print(len(scoreboard)-len_input-1)  # Part 2
    break

