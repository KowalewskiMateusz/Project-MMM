""""
A collection of helper funtions implementing simple matrix operations on
Python 2D-lists
"""

def mult_mat_square(a, b):
    """Returns a multiply of two square matrixes"""
    ans = []
    side = len(a)
    for i in range(side):
        ans.append([])
        for j in range(side):
            sum = 0
            for k in range(side):
                sum += a[i][k] * b[k][j]
            ans[i].append(sum)
    return ans

def scale_mat_square(a, k):
    """Returns a matrix with elements scaled by a factor of k"""
    ans = []
    for i in range(len(a)):
        ans.append([])
        for j in range(len(a[i])):
            ans[i].append(a[i][j] * k)
    return ans

def factorial(n):
    """Returns a factorial of n"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def add_mat_square(a, b):
    """Returns a sum of two square matrixes"""
    ans = []
    side = len(a)
    for i in range(side):
        ans.append([])
        for j in range(side):
            ans[i].append(a[i][j] + b[i][j])
    return ans

def identity(side):
    """Returns an identity matrix of a given order"""
    ans = []
    for i in range(side):
        ans.append([])
        for j in range(side):
            ans[i].append(0)
        ans[i][i] = 1
    return ans

def zeros(side):
    """Returns a zero-filled matrix of a given order"""
    ans = []
    for i in range(side):
        ans.append([])
        for j in range(side):
            ans[i].append(0)
    return ans

def exp_mat(a, k = 8):
    """
    Returns a matrix exponential using series approximation e^A = sum(A^k/k!).
    Parametr k specifies a number of series values used.
    """
    ans = add_mat_square(identity(len(a)), a)
    mult = a
    for i in range(k):
        mult = mult_mat_square(mult, a)
        ans = add_mat_square(ans, scale_mat_square(mult, 1/factorial(i+2)))
    return ans