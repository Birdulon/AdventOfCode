data = '3113322113'

def iterate(s):
  lastchar = s[0]
  lastcount = 1
  output = []
  for c in s[1:] + '\x00':
    if c == lastchar:
      lastcount += 1
    else:
      output += [str(lastcount), lastchar] # [lastchar]*lastcount
      lastchar = c
      lastcount = 1
  return ''.join(output)

s = data
for i in range(40):
  s = iterate(s)
print(len(s))  # Part 1
s2 = s
for i in range(10):  # equivalent to 50 times from starting input. Doesn't really save time though.
  s2 = iterate(s2)
print(len(s2))  # Part 2
