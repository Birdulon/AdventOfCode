with open('day16-input1', 'r') as file:
  data = [l.strip('\n') for l in file]
with open('day16-input2', 'r') as file:
  data2 = [l.strip('\n') for l in file]
import re
numbers_pt1 = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data if d]
numbers_pt2 = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data2 if d]

def oper_prototype(operator, immediate_a, immediate_b, regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = operator((a if immediate_a else regs[a]), (b if immediate_b else regs[b]))
  return r

addr = lambda regs, opcodes: oper_prototype(int.__add__, False, False, regs, opcodes)
addi = lambda regs, opcodes: oper_prototype(int.__add__, False, True, regs, opcodes)
mulr = lambda regs, opcodes: oper_prototype(int.__mul__, False, False, regs, opcodes)
muli = lambda regs, opcodes: oper_prototype(int.__mul__, False, True, regs, opcodes)
andr = lambda regs, opcodes: oper_prototype(int.__and__, False, False, regs, opcodes)
andi = lambda regs, opcodes: oper_prototype(int.__and__, False, True, regs, opcodes)
orr = lambda regs, opcodes: oper_prototype(int.__or__, False, False, regs, opcodes)
ori = lambda regs, opcodes: oper_prototype(int.__or__, False, True, regs, opcodes)
setr = lambda regs, opcodes: oper_prototype(lambda a, b: a, True, True, regs, opcodes)
seti = lambda regs, opcodes: oper_prototype(lambda a, b: a, False, True, regs, opcodes)
gtir = lambda regs, opcodes: oper_prototype(int.__gt__, True, False, regs, opcodes)
gtri = lambda regs, opcodes: oper_prototype(int.__gt__, False, True, regs, opcodes)
gtrr = lambda regs, opcodes: oper_prototype(int.__gt__, False, False, regs, opcodes)
eqir = lambda regs, opcodes: oper_prototype(int.__eq__, True, False, regs, opcodes)
eqri = lambda regs, opcodes: oper_prototype(int.__eq__, False, True, regs, opcodes)
eqrr = lambda regs, opcodes: oper_prototype(int.__eq__, False, False, regs, opcodes)

instructions = [addr, addi, mulr, muli, andr, andi, orr, ori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

num_3_or_more = 0
instruction_codes = {}
instruction_impossibilities = {}
for before, opcodes, after in zip(numbers_pt1[::3], numbers_pt1[1::3], numbers_pt1[2::3]):
  possibilities = set()
  impossibilities = set()
  for op in instructions:
    try:
      r2 = op(before, opcodes)
      if r2 == after:
        possibilities.add(op)
      else:
        impossibilities.add(op)
    except:
      impossibilities.add(op)
  if len(possibilities) >= 3:
    num_3_or_more += 1

  if opcodes[0] in instruction_codes:
    instruction_codes[opcodes[0]] &= possibilities
  else:
    instruction_codes[opcodes[0]] = set(possibilities)

  if opcodes[0] in instruction_impossibilities:
    instruction_impossibilities[opcodes[0]] |= impossibilities
  else:
    instruction_impossibilities[opcodes[0]] = set(impossibilities)

print(num_3_or_more)  # Part 1

for k in instruction_codes:
  instruction_codes[k] -= instruction_impossibilities[k]
while sum([len(i) for i in instruction_codes.values()]) > len(instructions):
  for code, cands in instruction_codes.items():
    if len(cands) == 1:
      for code2 in [c for c in instruction_codes if c != code]:
        instruction_codes[code2] -= cands

opcode_convert = {code: list(s)[0] for code, s in instruction_codes.items()}

regs = [0, 0, 0, 0]
for i, opcodes in enumerate(numbers_pt2):
  try:
    regs = opcode_convert[opcodes[0]](regs, opcodes)
  except:
    print(f'Line {i}: {regs}  {opcodes}')
    raise

print(regs)  # Part 2 is first number

