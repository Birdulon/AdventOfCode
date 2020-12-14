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
  return m_set, fork_str

mem = {}
fork_str = ''
xs = 0
m_set = 0
for line in lines:
  tokens = line.split()
  if tokens[0] == 'mask':
    fork_str = tokens[-1]  #.replace('X', '{}')
    xs = fork_str.count('X')
    m_set = int(tokens[-1].replace('X', '0'), 2)
  elif tokens[0][:3] == 'mem':
    val = int(tokens[-1])
    addr = f'{int(tokens[0][4:-1]) | m_set:036b}'
    addr = ''.join(['{}' if f=='X' else c for c,f in zip(addr, fork_str)])
    addrs = [addr.format(*f'{i:0{xs}b}') for i in range(2**xs)]
    for a in addrs:
      mem[a] = val
print(f'Part 2: {sum(mem.values())}')
