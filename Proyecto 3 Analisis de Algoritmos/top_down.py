


def top_down(i, j, M, X, Y):
	if M[i][j] == float('inf'):
		if i == 0 or j == 0:
			M[i][j] = -2*(i+j)
		else:
			if X[i-1] == Y[j-1]: r = 1
			else: r = -1
			m1 = top_down(i-1, j  , M, X, Y) - 2
			m2 = top_down(i  , j-1, M, X, Y) - 2
			m3 = top_down(i-1, j-1, M, X, Y) + r
			M[i][j] = max(m1, m2, m3)

	return M[i][j]


X = 'GAAC'
Y = 'CAAGAC'
i = len(X)
j = len(Y)


M = [ [float('inf')]*(j+1) for _ in range(i+1) ]

top_down(i, j, M, X, Y)

a = []
b = []
a.append(X[i-1])
b.append(Y[j-1])

while i != 0 or j != 0:
	m = max( M[i-1][j], M[i][j-1], M[i-1][j-1] )
	if m == M[i-1][j]:
		i = i-1
		a.append(X[i-1])
		b.append('-')

	if m == M[i][j-1]:
		j = j-1
		a.append('-')
		b.append(Y[j-1])

	if m == M[i-1][j-1]:
		i = i-1
		j = j-1
		a.append(X[i-1])
		b.append(Y[j-1])
		
for m in M:
	print(m)

print(''.join(reversed(b)), "CAAGAC")
print(''.join(reversed(a)), "GAA--C")

