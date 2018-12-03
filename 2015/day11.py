data = 'cqjxjnds'
#import numpy as np
#base26m = np.array([26**n for n in range(7, -1, -1)], dtype=np.int64)
#def increment(s):
  #digits = [ord(c)-97 for c in s]
  #base26 = np.dot(base26m, digits)
  #num = base26 + 1
  #digits2 = []
  #while num:
    #digits2.append(num % 26)
    #num //= 26
  #digits2 += [0]*(8-len(digits2))
  #return ''.join([chr(d+97) for d in reversed(digits2)])

def increment(s):
  if 'a' <= s[-1] < 'z':
    inc = 2 if s[-1] in 'hnk' else 1
    return s[:-1] + chr(ord(s[-1])+inc)
  else:
    return increment(s[:-1]) + 'a'

def is_valid(s):
  #if 'i' in s or 'o' in s or 'l' in s:
    #return False
  straight = False
  for a, b, c in zip(s[:-2], s[1:-1], s[2:]):
    if ord(a) == ord(b)-1 == ord(c)-2:
      straight = True
      break
  if not straight:
    return False
  pairs = set()
  for a, b in zip(s[:-1], s[1:]):
    if a == b:
      pairs.add(a)
    if len(pairs) >= 2:
      return True
  return False

password = increment(data)
while not is_valid(password):
  password = increment(password)
print(password)  # Part 1  -- cqkkaabc is not correct?! - actually cqjxxyzz

password2 = increment(password)
while not is_valid(password2):
  password2 = increment(password2)
print(password2)  # Part 2
