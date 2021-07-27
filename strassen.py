import random
import math
import sys

def create_mat(dim):
    matrix = [[0 for _ in range(dim)] for _ in range(dim)]

    for i in range(dim):
        for j in range(dim):
            matrix[i][j] = random.randint(0, 1)

    return matrix

def sum_mat(C):
    count = 0
    for i in range(len(C)):
        for j in range(len(C)):
            count += C[i][j]
    return count

def diag_sum(C):
    count = 0
    for i in range(len(C)):
        count += C[i][i]
    return count

def naive_mult(A, B, dim):
    new_mat = [[0 for _ in range(dim)] for _ in range(dim)]

    # iterate through rows of A & C
    for i in range(dim):
        # iterate through columns of B
        for k in range(dim):
            # iterate through columns of A & rows of B
            for j in range(dim):
                new_mat[i][j] += A[i][k] * B[k][j]

    return new_mat

def create_graph(dim, p):
    G = [[0 for _ in range(dim)] for _ in range(dim)]
   
    for i in range(dim):
        for j in range(i + 1):
            if random.random() < p and i != j: 
                G[i][j] = 1
                G[j][i] = 1
    return G 

def count_triangle(dim, p):
    G = create_graph(dim, p)
    G_cube = strassen_helper(G, strassen_helper(G, G, dim, n0), dim, n0)
    return (diag_sum(G_cube)) / 6

def add_mat(A, B, dim):
    return [[i + j for (i, j) in zip(A[k], B[k])] for k in range(0, dim)]

def sub_mat(A, B, dim):
    return [[i - j for (i, j) in zip(A[k], B[k])] for k in range(0, dim)]

def strassen_helper(A, B, dim, n0):
    # switch to conventional below cross-over 
    if dim <= n0 or dim == 1: 
         return naive_mult(A, B, dim)
    else: 
        s = int(dim / 2) 
  
        A_prime =  [ [], [], [], [] ]
        B_prime =  [ [], [], [], [] ]
        C = [ [], [], [], [] ]

        R = [[0 for _ in range(dim)] for _ in range(dim)]

        # initializing A sub-arrays to 0
        for k in range (0, 4): 
            for i in range (0, s):
                A_prime[k].append(([0] * s))
                B_prime[k].append(([0] * s))


        for i in range(0, s): 
            for j in range(0, s): 
                A_prime[0][i][j] = A[i][j] #top left
                A_prime[1][i][j] = A[i][j + s] #top right
                A_prime[2][i][j] = A[i + s][j] #bottom left
                A_prime[3][i][j] = A[i + s][j + s] #bottom right
                B_prime[0][i][j] = B[i][j] #top left
                B_prime[1][i][j] = B[i][j + s] #top right
                B_prime[2][i][j] = B[i + s][j] #bottom left 
                B_prime[3][i][j] = B[i + s][j + s] #bottom right

        a = A_prime[0]
        b = A_prime[1]
        c = A_prime[2]
        d = A_prime[3]
        e = B_prime[0]
        f = B_prime[1]
        g = B_prime[2]
        h = B_prime[3]

        p1 = strassen_helper(a, sub_mat(f, h, s), s, n0)
        p2 = strassen_helper(add_mat(a, b, s), h, s, n0)
        p3 = strassen_helper(add_mat(c, d, s), e, s, n0)
        p4 = strassen_helper(d, sub_mat(g, e, s), s, n0)
        p5 = strassen_helper(add_mat(a, d, s), add_mat(e, h, s), s, n0)
        p6 = strassen_helper(sub_mat(b, d, s), add_mat(g, h, s), s, n0)
        p7 = strassen_helper(sub_mat(a, c, s), add_mat(e, f, s), s, n0)

        C[0] = sub_mat(add_mat(p5, p4, s), sub_mat(p2, p6, s), s)
        C[1] = add_mat(p1, p2, s)
        C[2] = add_mat(p3, p4, s)
        C[3] = sub_mat(add_mat(p1, p5, s), add_mat(p3, p7, s), s)

        for i in range(s):
            R[i] = C[0][i] + C[1][i]
            R[i + s] =  C[2][i] + C[3][i]

        return R

def strassen(A, B, dim, n0):
    if ((dim & (dim - 1) == 0) and dim != 0): 
        return strassen_helper(A, B, dim, n0)
    else: 
        next_exp_of_two = math.ceil(math.log(dim, 2))
        pad =  (2 ** next_exp_of_two) - dim

        # pad matrix to size of next power of two with 0's
        for i in range(dim):
            A[i].extend([0] * pad)
            B[i].extend([0] * pad)
        
        for i in range(pad):
            A.append([0] * (dim + pad))
            B.append([0] * (dim + pad))

        new_dim = dim + pad

        return strassen_helper(A, B, new_dim, n0)

if __name__ == "__main__":
    n0 = 32
    dim = int(sys.argv[2])
    inputfile = sys.argv[3]

    # initialize matrices
    A = [[0 for _ in range(dim)] for _ in range(dim)]
    B = [[0 for _ in range(dim)] for _ in range(dim)]

    with open(f'{inputfile}', 'r') as f:
        dim2 = dim ** 2

        for i, val in enumerate(f):
            # populate matrix A
            if i < dim2:
                A[i // dim][i % dim] = int(val)
            # populate matrix B
            else:
                B[(i - dim2) // dim][(i - dim2) % dim] = int(val)

    C = strassen(A, B, dim, n0)

    # print diagonal
    for i in range(dim):
        print(C[i][i]) 
