with open('day16-input1', 'r') as file:
  data = [l.strip('\n') for l in file]
with open('day16-input2', 'r') as file:
  data2 = [l.strip('\n') for l in file]
import re
numbers_pt1 = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data if d]
numbers_pt2 = [[int(s) for s in re.findall(r'-?\d+', d)] for d in data2 if d]


class oper_factory:
  def __init__(self, operator, immediate_a, immediate_b):
    self.operator = operator
    self.immediate_a = immediate_a
    self.immediate_b = immediate_b

  def __call__(self, regs, opcodes):
    op, a, b, c = opcodes
    r = list(regs)
    r[c] = self.operator((a if self.immediate_a else regs[a]), (b if self.immediate_b else regs[b]))
    return r

bin_ops = (int.__add__, int.__mul__, int.__and__, int.__or__)
set_op = lambda a, b: a  # Just discard second operand
comp_ops = (int.__gt__, int.__eq__)
comp_imms = ((True, False), (False, True), (False, False))  # ir, ri, rr

instructions = [oper_factory(op, False, imm) for op in bin_ops for imm in (False, True)] \
             + [oper_factory(set_op, imm, True) for imm in (False, True)] \
             + [oper_factory(op, *imm) for op in comp_ops for imm in comp_imms]


samples_3_or_more = 0
instruction_candidates = {}
for before, opcodes, after in zip(numbers_pt1[::3], numbers_pt1[1::3], numbers_pt1[2::3]):
  possibilities = set()
  for op in instructions:
    try:
      r2 = op(before, opcodes)
      if r2 == after:
        possibilities.add(op)
    except Exception:
      pass
  if len(possibilities) >= 3:
    samples_3_or_more += 1

  if opcodes[0] in instruction_candidates:
    instruction_candidates[opcodes[0]] &= possibilities
  else:
    instruction_candidates[opcodes[0]] = set(possibilities)

print(samples_3_or_more)  # Part 1

instruction_codes = {}
while instruction_candidates:
  for code, candidates in instruction_candidates.items():
    if len(candidates) == 1:
      instruction_codes[code] = tuple(candidates)[0]
      for code2 in [c for c in instruction_candidates if c != code]:
        instruction_candidates[code2].discard(instruction_codes[code])
      instruction_candidates.pop(code)
      break  # Can't continue iterating on mutated sequence, also want to recheck start anyway

regs = [0, 0, 0, 0]
for i, opcodes in enumerate(numbers_pt2):
  regs = instruction_codes[opcodes[0]](regs, opcodes)

print(regs)  # Part 2 is first number

