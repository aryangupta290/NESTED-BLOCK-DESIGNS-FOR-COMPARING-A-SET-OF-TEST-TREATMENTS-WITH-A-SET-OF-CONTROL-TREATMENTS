import numpy as np


def get_efficiency(N, v1, v2, b, k):
    # N: Block/Sub-Block Matrix
    # v1: number of test treatments
    # v2: number of control treatments
    # b: number of blocks/sub-blocks.
    # k: Size of block/sub-block
    kby2 = int(np.floor(k/2))
    min_val = float('inf')
    for x in range(kby2):
        for z in range(b+1):
            if x == 0 and z == 0:
                g = float('inf')
            else:
                a = v2 * (v1-1)**2
                d = v1 * (v2 - 1)
                C = b * x + z
                A = (k * C - v2 * (b * x * x + 2 * x * z + z)) / (v1 * k)
                B = (b * k * v1 * (k - 1) - v2 * C * (v1 * (k - 1) + k) +
                     v2 * v2 * (b * x * x + 2 * x * z + z)) / (v1 * k)
                if A == 0 or B == 0 or C == 0:
                    continue
                g = 1 / A + a / B + d / C
            if g < min_val:
                min_val = g
    LB = min_val
    # N1 is of size (v1+v2)*b
    # It is the freqwency matrix
    N1 = np.zeros((v1+v2, b))
    for block in range(b):
        for treatment in N[block]:
            N1[treatment-1][block] += 1
    # convert N1 to int type
    N1 = N1.astype(int)
    rvec = np.dot(N1, np.ones((b, 1)))
    rvec = rvec.astype(int)
    v = v1 + v2
    R = np.zeros((v, v))
    for i in range(v):
        R[i][i] = rvec[i]
    NNP = np.dot(N1, N1.T)
    M = R - NNP/k
    Minv = np.linalg.pinv(M)
    onev2 = np.ones((v2, 1))
    onev1 = np.ones((v1, 1))
    iv2 = np.zeros((v2, v2))
    for i in range(v2):
        iv2[i][i] = 1
    iv1 = np.zeros((v1, v1))
    for i in range(v1):
        iv1[i][i] = 1
    outer_product1 = np.kron(onev2, iv1)
    outer_product2 = -np.kron(iv2, onev1)
    P = np.concatenate((outer_product1, outer_product2), axis=1)
    T = np.dot(P, np.dot(Minv, P.T))
    temp = 0
    for i in range(T.shape[0]):
            temp += T[i][i]
    e = min_val / temp
    return e
