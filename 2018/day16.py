with open('day16-input1', 'r') as file:
  data = [l.strip('\n') for l in file]
with open('day16-input2', 'r') as file:
  data2 = [l.strip('\n') for l in file]
import numpy as np
import re


numbers = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data if d]
numbers2 = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data2 if d]
# arr = np.array(numbers, dtype=np.int64)

registers = np.zeros(4, dtype=np.int64)

def addr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] + regs[b]
  return r

def addi(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] + b
  return r

def mulr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] * regs[b]
  return r

def muli(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] * b
  return r

def andr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] & regs[b]
  return r

def andi(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] & b
  return r

def orr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] | regs[b]
  return r

def ori(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a] | b
  return r

def setr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = regs[a]
  return r

def seti(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = a
  return r

def gtir(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(a > regs[b]))
  return r

def gtri(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(regs[a] > b))
  return r

def gtrr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(regs[a] > regs[b]))
  return r

def eqir(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(a == regs[b]))
  return r

def eqri(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(regs[a] == b))
  return r

def eqrr(regs, opcodes):
  op, a, b, c = opcodes
  r = list(regs)
  r[c] = int(bool(regs[a] == regs[b]))
  return r

instructions = [addr, addi, mulr, muli, andr, andi, orr, ori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

num_3_or_more = 0
instruction_codes = {}
instruction_impossibilities = {}
for before, opcodes, after in zip(numbers[::3], numbers[1::3], numbers[2::3]):
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
for i, opcodes in enumerate(numbers2):
  try:
    regs = opcode_convert[opcodes[0]](regs, opcodes)
  except:
    print(f'Line {i}: {regs}  {opcodes}')
    raise

print(regs)  # Part 2 is first number

