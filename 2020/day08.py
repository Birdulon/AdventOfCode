with open('input08', 'r') as file:
  lines = [(lambda x: (x[0],int(x[1])))(line.strip().split()) for line in file.readlines()]

def f_acc(regs, x):
  regs['acc'] += x
  regs['ip'] += 1

def f_jmp(regs, x):
  regs['ip'] += x

def f_nop(regs, x):
  regs['ip'] += 1

fns = {'acc': f_acc, 'jmp': f_jmp, 'nop': f_nop}
inst_swap = {'jmp': 'nop', 'nop': 'jmp', 'acc': 'acc'}

regs = {'ip': 0, 'acc': 0}
executed_ips = set()
while(True):
  if regs['ip'] in executed_ips:
    print(f'Part 1: {regs["acc"]}')
    break
  executed_ips.add(regs['ip'])
  inst, x = lines[regs['ip']]
  fns[inst](regs, x)

# This was an attempt to do a clever backtracking approach to minimize runs. It didn't work properly.
#regs = {'ip': 0, 'acc': 0}
#stacktrace = []
#executed_ips = set()
#flipped_ips = set()
#while True:
  #if regs['ip'] in executed_ips:
    #while regs['ip'] in flipped_ips:
      #regs, executed_ips = stacktrace.pop()
    #print(f'loop reached, backtracking to state {regs}')
    #inst, x = lines[regs['ip']]
    #inst = inst_swap[inst]
    #flipped_ips.add(regs['ip'])
  #else:
    #executed_ips.add(regs['ip'])
    #inst, x = lines[regs['ip']]
  #stacktrace.append((regs.copy(), executed_ips.copy()))
  #fns[inst](regs, x)
  #if regs['ip'] >= len(lines):
    #print('Program completed successfully!')
    #break


# Turns out the problemspace is so low that bruteforce is king anyway
def simulate(flipped_ip):
  regs = {'ip': 0, 'acc': 0}
  executed_ips = set()
  while True:
    if regs['ip'] in executed_ips:
      return False
    executed_ips.add(regs['ip'])
    inst, x = lines[regs['ip']]
    if regs['ip'] == flipped_ip:
      inst = inst_swap[inst]
    fns[inst](regs, x)
    if regs['ip'] >= len(lines):
      return regs['acc']

for i, (inst, x) in enumerate(lines):
  if inst != 'acc':
    result = simulate(i)
    if result:
      print(f'Part 2: {result}')
      break
