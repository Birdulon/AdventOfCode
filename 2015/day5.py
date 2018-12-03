with open('day5-input', 'r') as file:
  data = [l.strip('\n') for l in file]

naughty_substrings = ['ab', 'cd', 'pq', 'xy']
vowels = set(['a', 'e', 'i', 'o', 'u'])
def is_nice(s):
  for n in naughty_substrings:
    if n in s:
      return False
  v_count = 0
  rep_count = 0
  last_char = ''
  for c in s:
    if c in vowels:
      v_count += 1
    if c == last_char:
      rep_count += 1
    last_char = c
  return v_count >= 3 and rep_count > 0
print(len([s for s in data if is_nice(s)]))  # Part 1

def is_nice2(s):
  spaced_rep = False
  for a, b in zip(s[:-2], s[2:]):
    if a == b:
      spaced_rep = True
      break
  if not spaced_rep:
    return False
  for a, b in zip(s[:-1], s[1:]):
    if s.count(a+b) > 1:
      return True
  return False
print(len([s for s in data if is_nice2(s)]))  # Part 2
