import numpy as np


def Trace(v1, v2, b, k, N):
    rvec = np.dot(N, np.ones((b, 1)))
    v = v1 + v2
    R = np.zeros((v, v))
    for i in range(v):
        R[i][i] = rvec[i]
    NNP = np.dot(N, N.T)
    C = R - NNP/k
    A = C[:v1, :v1]
    D = C[v1:v, v1:v]
    f1b = np.trace(A)/v1
    f4b = np.trace(D)/v2
    f2b = (np.sum(A) - v1*f1b)/(v1*(v1-1))
    f5b = (np.sum(D) - v2*f4b)/(v2*(v2-1))
    out = v2*(v1-1)/(f1b - f2b) + v1*(v2-1)/(f4b - f5b) + v2/(f1b + (v1-1)*f2b)
    return out


def MinTrace(v1, v2, b, k, r0):
    Q1 = r0*r0/b
    temp = k * r0 - v2*Q1
    t1 = v1*k/temp
    t2 = v1 * (v2-1)/r0
    temp = b*v1*k*(k-1) - (v1*(k-1)+k)*v2*r0 + Q1*(v2**2)
    t3 = (v1*v2*k*(v1-1) * (v1-1))/temp
    out = t1 + t2 + t3
    return (out)


def get_efficiency(v1, v2, d):
    # v1: number of test treatments
    # v2: number of control treatments
    # d: block/sub-block design
    b = d.shape[0]
    k = d.shape[1]
    N = np.zeros((v1+v2, b))
    for block in range(b):
        for treatment in d[block]:
            N[treatment-1][block] += 1
    N = N.astype(int)
    rvec = np.dot(N, np.ones((b, 1)))
    r0 = int(np.floor(np.mean(rvec[v1:v1+v2])))
    trd = Trace(v1, v2, b, k, N)
    mintrace = MinTrace(v1, v2, b, k, r0)
    e = mintrace/trd
    return e
