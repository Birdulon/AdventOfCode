for i in range(1, 500001):
  presents = 0
  for n in range(1, i+1):
    if i%n == 0:
      presents += 10*n
  if presents >= 33100000:
    print(i, presents)
    break
