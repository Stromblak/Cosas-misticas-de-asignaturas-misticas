


def top_down(i, j, M, X, Y, B):
	if M[i][j] == float('inf'):
		if i == 0 or j == 0:
			M[i][j] = -2*(i+j)
		else:
			if X[i-1] == Y[j-1]: r = 1
			else: r = -1
			m1 = top_down(i-1, j  , M, X, Y, B) - 2
			m2 = top_down(i  , j-1, M, X, Y, B) - 2
			m3 = top_down(i-1, j-1, M, X, Y, B) + r
			
			M[i][j] = max(m1, m2, m3)
			if M[i][j] == m1: B[i][j] = (i-1, j)
			elif M[i][j] == m2: B[i][j] = (i, j-1)
			else: B[i][j] = (i-1, j-1)

	return M[i][j]


X = 'CCAAT T AG'
Y = 'CAAT T T G'
i = len(X)
j = len(Y)

M = [ [float('inf')]*(j+1) for _ in range(i+1) ]
B = [ [(0, 0)]*(j+1) for _ in range(i+1) ]


top_down(i, j, M, X, Y, B)

a = []
b = []
while i != 0 or j != 0:
	if B[i][j][0] == i:
		a.append('-')
	else:
		a.append(X[i-1])

	if B[i][j][1] == j:
		b.append('-')
	else:
		b.append(Y[j-1])
		
	i, j = B[i][j]

	


print(''.join(reversed(b)))
print('C-AAT T T G')
print()
print(''.join(reversed(a)))
print('CCAAT T A-G')
