l=open('input/6','r').read()
def s(n,skip=0):
	for i in range(max(skip, n),len(l)):
		if len(set(l[i-n:i]))==n:
			return i

for i in range(100000):
	four = s(4)
	fourteen = s(14, four)
print(four)
print(fourteen)
