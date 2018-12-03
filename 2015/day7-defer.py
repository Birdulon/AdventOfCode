with open('day7-input', 'r') as file:
  data = [l.strip('\n') for l in file]
TOKENS = [line.split(' ') for line in data]
bin_ops = {'AND': int.__and__, 'OR': int.__or__, 'RSHIFT': int.__rshift__, 'LSHIFT': int.__lshift__}

class dict_int_giver(dict):
  def __init__(self, kvs=[], readonly=None):
    super().__init__(kvs)
    self.readonly = set()
    if readonly:
      self.readonly = set(readonly)
  def __getitem__(self, key):
    try:
      return int(key.replace(',', ''))
    except ValueError:
      return dict.get(self, key, None)
  def __setitem__(self, key, value):
    if key in self.readonly:
      return
    dict.__setitem__(self, key, value)

def run_circuit(identifiers):
  stack = [line for line in reversed(TOKENS)]

  deferred = {}
  def defer(until_identifier, tokens):
    if until_identifier in deferred:
      deferred[until_identifier].append(tokens)
    else:
      deferred[until_identifier] = [tokens]

  while stack:
    tokens = stack.pop()
    output = tokens[-1]
    input = tokens[:-2]
    if len(input) == 1:  # Can only be a -> b
      i = identifiers[input[0]]
      if i is not None:
        identifiers[output] = i
        if output in deferred:
          stack += deferred.pop(output)
      else:
        defer(input[0], tokens)
    elif len(input) == 2:  # Can only be NOT a -> b. a must be identifier.
      if input[1] in identifiers:
        identifiers[output] = identifiers[input[1]] ^ 0xFFFF  # 16bit values
        if output in deferred:
          stack += deferred.pop(output)
      else:
        defer(input[1], tokens)
    elif len(input) == 3:  # Can be any of the binary operators
      i = identifiers[input[0]]
      j = identifiers[input[2]]
      if i is None:
        defer(input[0], tokens)
        continue
      if j is None:
        defer(input[2], tokens)
        continue
      identifiers[output] = bin_ops[input[1]](i, j) & 0xFFFF
      if output in deferred:
        stack += deferred.pop(output)

identifiers_1 = dict_int_giver()
run_circuit(identifiers_1)
print(identifiers_1['a'])  # Part 1
identifiers_2 = dict_int_giver([ ['b', identifiers_1['a'] ] ], ['b'])
run_circuit(identifiers_2)
print(identifiers_2['a'])  # Part 2
