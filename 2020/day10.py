import numpy as np

# Load input
with open('input10', 'r') as f:
  data = [0] + sorted([int(l) for l in f.readlines()])  # NB: We add the 0J source ourselves
n_data = np.array(data)

# Part 1: Connect all of them together
diff = n_data[1:] - n_data[:-1]
# Confirm this by multiplying the 1J differences with the 3J differences.
# NB: we treat the internal adapter 3J difference as an off-by-one for simplicity.
print('Part 1: ', (diff==1).sum() * (1 + (diff==3).sum()))

# Part 2: Find the number of possible chains
n_possibilities = {data[-1]: 1}  # The highest one can only connect to the internal adapter.
for i in reversed(data[:-1]):  # We've already done the highest one as a special case
  delta = n_data - i
  p = 0
  for n in n_data[np.logical_and(delta<=3, delta>0)]:  # You could probably plug two of the same together, but our input doesn't require us to handle that, and this simplifies things ;)
    p += n_possibilities[n]
  n_possibilities[i] = p
print('Part 2: ', n_possibilities[0])
