import numpy as np
max_it = 813960  # Somewhat cheaty - this value was obtained from an earlier factor-based brute force. Just use an arbitrarily large number if it fails.
input = 33100000

houses = np.ones([max_it], dtype=np.int64)
pres10 = input//10
for i in range(2, max_it):
  houses[i::i] += i
print(np.argmax(houses > pres10))  # Part 1

houses_2 = np.ones([max_it], dtype=np.int64)
pres11 = input//11
for i in range(2, max_it):
  houses_2[i:i*51:i] += i
print(np.argmax(houses_2 > pres11))  # Part 2
