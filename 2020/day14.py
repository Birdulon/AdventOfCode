with open('input14', 'r') as file:
  lines = [l.strip() for l in file.readlines()]

def masks(m):
  m_reset = int(m.replace('X', '1'), 2)
  m_set = int(m.replace('X', '0'), 2)
  return m_reset, m_set

mem = {}
m_reset = 0xFFFFFFFFFFFFFFFF
m_set = 0
for line in lines:
    tokens = line.split()
    if tokens[0] == 'mask':
        m_reset, m_set = masks(tokens[-1])
    elif tokens[0][:3] == 'mem':
        mem[int(tokens[0][4:-1])] = int(tokens[-1]) & m_reset | m_set
print(f'Part 1: {sum(mem.values())}')


def mem_masks(m):
  fork_bits = [i for i, x in enumerate(reversed(m)) if x=='X']
  m_set = int(m.replace('X', '0'), 2)
  return m_set, fork_bits

def fork_address(addrs, bits):
  if len(bits) == 1:
    return [a for addr in addrs for a in (addr, addr^(1<<bits[0]))]
  a2s = fork_address(addrs, bits[1:])
  return a2s + [a^(1<<bits[0]) for a in a2s]

mem = {}
fork_bits = []
m_set = 0
for line in lines:
  tokens = line.split()
  if tokens[0] == 'mask':
    m_set, fork_bits = mem_masks(tokens[-1])
  elif tokens[0][:3] == 'mem':
    val = int(tokens[-1])
    addr = int(tokens[0][4:-1]) | m_set
    addrs = [addr]
    if len(fork_bits) > 0:
      addrs = addrs + fork_address(addrs, fork_bits)
    for a in addrs:
      mem[a] = val
print(f'Part 2: {sum(mem.values())}')
