from helpers import *
lines = read_day(25).split('\n')
snafu_digits = {'=':-2, '-':-1, '0':0, '1':1, '2':2}
# minimal_snafus = [-2]
# for i in range(1, 50):
# 	minimal_snafus.append(minimal_snafus[-1] + (-2 * (5**i)))
# print(minimal_snafus)

def snafu_to_decimal(s: str) -> int:
	return sum((snafu_digits[v] * (5**i) for i,v in enumerate(reversed(s))))

def decimal_to_snafu(i: int) -> str:
	# We don't want to constantly flip addition/subtraction, so start with biggest number and subtract
	digits = 0
	maximal = 0
	while i > maximal:
		maximal += 2 * (5**digits)
		digits += 1
	base5 = np.base_repr(maximal-i, 5)
	s = ['2'] * digits
	for i,d in enumerate(reversed(base5)):
		s[i] = {'0':'2', '1':'1', '2':'0', '3':'-', '4':'='}[d]
	return ''.join(reversed(s))

# print(decimal_to_snafu(1747))
print(f'Part 1: {decimal_to_snafu(sum((snafu_to_decimal(l) for l in lines)))}')
