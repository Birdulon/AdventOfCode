with open('day21-input', 'r') as file:
  data = [l.strip('\n') for l in file]

# This solution includes optimisations which only work for this input.
# To adapt it to other inputs, the exit condition must be identified and the other optimisations removed.

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
inst_names = ('addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr')
insts = {name: func for name, func in zip(inst_names, instructions)}

ops = {}
ops['seti'] = 0

registers = [0,0,0,0,0,0]
ip_r = int(data[0].split()[-1])
tokens_ = []
for line in data[1:]:
  tokens = line.split()
  tokens_.append([insts[tokens[0]]] + [int(i) for i in tokens[1:]])


def run_program(initial_registers):
  registers = initial_registers.copy()
  past_comps = set()
  past_comps_l = []
  for j in range(100000000000):
    # print(registers)
    try:
      i = registers[ip_r]
      if i == 17:
        registers[1] = (registers[3]//256)-1
        registers[ip_r] += 1
        continue
      if i == 9:
        registers[5] = (((registers[5]+registers[1])&0xFFFFFF) * 65899) & 0xFFFFFF
        registers[ip_r] = 13
        continue
      if i == 28:
        # print(registers)
        if registers[5] in past_comps:
          # print('Loop???')
          return past_comps_l
        past_comps.add(registers[5])
        past_comps_l.append(registers[5])
      opcodes = tokens_[i]
      registers = opcodes[0](registers, opcodes)
    except Exception:
      print(f'Halted at cycle {j}!')
      return j
    registers[ip_r] += 1
  print(f'Did not halt! {registers}')
  return 1000000

past_comps_l = run_program([0,0,0,0,0,0])
print(past_comps_l[0])  # Part 1
print(past_comps_l[-1])  # Part 2

# #ip 2
# L00 - seti 123 0 5
# L01 - bani 5 456 5
# L02 - eqri 5 72 5    - r5 = (r5 == 72)
# L03 - addr 5 2 2     - r2 += r5
# L04 - seti 0 0 2     - r2 = 0 (goto L01)
# L05 - seti 0 9 5     - r5 = 0
# L06 - bori 5 65536 3     - r3 = r5 | 0x010000  <-- Insertion point after comparison
# L07 - seti 7586220 4 5   - r5 = 7586220
# [FUNCTION]
# L08 - bani 3 255 1       - r1 = r3 & 0xFF  <-- insertion point
# L09 - addr 5 1 5         - r5 += r1
# L10 - bani 5 16777215 5  - r5 &= 0x00FFFFFF
# L11 - muli 5 65899 5     - r5 *= 65899
# L12 - bani 5 16777215 5  - r5 &= 0x00FFFFFF
# L13 - gtir 256 3 1       - r1 = 256 > r3  (not if executed sequentially)
# L14 - addr 1 2 2         - r2 += r1 (goto L16->L28 if 256>r3)  !!!
# L15 - addi 2 1 2         - r2 += 1 (goto L17)
# L16 - seti 27 9 2   - r2 = 27 (goto L28 - comparison)

# L17 - seti 0 9 1         - r1 = 0
# [FUNCTION]
# L18 - addi 1 1 4         - r4 = r1 + 1  <-- insertion point
# L19 - muli 4 256 4       - r4 *= 256
# L20 - gtrr 4 3 4         - r4 = r4 > r3
# L21 - addr 4 2 2   - r2 += r4 (goto L23->L26 if (r1+1)*256 > r3. r3=r1 then goto L08)
# L22 - addi 2 1 2   - r2 += 1 (goto L24 increment r1 and goto L18)
# [FUNCTION]
# L28 - eqrr 5 0 1   - r1 = r5==r0    - Exit condition!  - 11050031 is lowest
# L29 - addr 1 2 2   - r2 += r1
# L30 - seti 5 0 2   - r2 = 5         - Goto L06



# L23 - seti 25 4 2  - r2 = 25 (goto L26)
# L24 - addi 1 1 1   - r1 += 1
# L25 - seti 17 2 2  - r2 = 17 (goto L18)
# L26 - setr 1 6 3   - r3 = r1
# L27 - seti 7 8 2   - r2 = 7 (goto L08)