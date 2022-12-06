l=open('input/6','r').read()
def s(n):
	for i in range(n,len(l)):
		if len(set(l[i-n:i]))==n:
			return print(i)
s(4)
s(14)