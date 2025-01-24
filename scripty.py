import sympy as sp
from sympy import pprint
# Define the matrix
A = sp.Matrix([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, ],
    [0, 0, 0, 1, 0, 0, ],
    [0, 0, 0, 0, 1, 0,],
    [0, 0, 0, 0, 0, 1, ],
    [0, 0, 0, 0, 0, 0, ]
])
_, ro = A.rref()
print(ro)
# Compute the transpose
A_transpose = A.T

# Display the transpose
print("Transpose of the matrix:")
pprint(A_transpose)
p, r = A_transpose.rref()

pprint(p)
print(r)