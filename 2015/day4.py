data = 'yzbqklnj'
from hashlib import md5
i = 0
while True:
  i += 1
  if md5(f'{data}{i}'.encode('utf-8')).hexdigest().startswith('00000'):
    print(i)  # Part 1
    break

i -= 1  # Just in case the first hit was 6 zeros
while True:
  i += 1
  if md5(f'{data}{i}'.encode('utf-8')).hexdigest().startswith('000000'):
    print(i)  # Part 2
    break
