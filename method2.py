import csv
from prettytable import PrettyTable
import efficiency_merging
import numpy as np
import os


def get_params(design, sub_block_size):
    v = 0
    for row in design:
        for cur in row:
            if cur > v:
                v = cur
    b1 = len(design)
    r = 0
    for row in design:
        for cur in row:
            if cur == 1:
                r += 1
    k1 = (v*r)/b1
    k2 = sub_block_size
    b2 = (b1*k1)/k2
    lambda1 = ((k1-1)*r)/(v-1)
    lambda2 = ((k2-1)*r)/(v-1)
    k1 = int(k1)
    b2 = int(b2)
    k2 = int(k2)
    lambda1 = int(lambda1)
    lambda2 = int(lambda2)
    return [v, b1, b2, r, k1, k2, lambda1, lambda2]


def method2(nbib_design, sub_block_size, alpha,  v2):
    if (not isinstance(nbib_design, list)):
        print("Error: nbib_design must be a list")
        return -1
    for i in range(len(nbib_design)):
        for j in range(len(nbib_design[i])):
            nbib_design[i][j] = int(nbib_design[i][j])
    try:
        [v_, b1_, b2_, r_, k1_, k2_, lambda1_, lambda2_] = get_params(
            nbib_design, sub_block_size)
    except:
        print("Error: unable to get parameters from the nbib_design.")
        return -1

    if (v_ <= 0 or b1_ <= 0 or b2_ <= 0 or r_ <= 0 or k1_ <= 0 or k2_ <= 0 or lambda1_ <= 0 or lambda2_ <= 0):
        print("Error: all parameters must be positive integers.")
        return -1
    q_ = b2_/b1_
    q_ = int(q_)
    if (v_*r_ != b1_*k1_ or b1_*k1_ != b2_*k2_ or b2_*k2_ != q_*b1_*k2_):
        print("Error: v*r = b1*k1 = q*b1*k2 = b2*k2 should be satisfied.")
        return -1

    if ((v_-1)*lambda1_ != (k1_-1)*r_):
        print("Error: (v-1)*lambda1 = (k1-1)*r should be satisfied.")
        return -1

    if ((v_-1)*lambda2_ != (k2_-1)*r_):
        print("Error: (v-1)*lambda2 = (k2-1)*r should be satisfied.")
        return -1

    if ((v_-1)*(lambda1_ - q_*lambda2_) != (q_-1)*r_):
        print("Error: (v-1)*(lambda1 - q*lambda2) = (q-1)*r should be satisfied.")
        return -1

    if alpha*v2 >= v_:
        print("Atleast one test treatment should be left.")
        return -1

    v1 = v_ - alpha * v2
    start = v1+1
    nbbpb = nbib_design
    for i in range(v2):
        from_ = v_ - (v2-i)*alpha + 1
        to_ = v_ - (v2-i-1)*alpha
        for i in range(len(nbbpb)):
            for j in range(len(nbbpb[i])):
                if nbbpb[i][j] >= from_ and nbbpb[i][j] <= to_:
                    nbbpb[i][j] = start
        start += 1

    b1 = b1_
    b2 = b2_
    r1 = r_
    r2 = alpha * r_
    k1 = k1_
    k2 = k2_
    lambda111 = lambda1_
    lambda112 = alpha * lambda1_
    lambda122 = alpha * alpha * lambda1_
    lambda211 = lambda2_
    lambda212 = alpha * lambda2_
    lambda222 = alpha * alpha * lambda2_
    print("NBBPB Design: ")
    for row in nbbpb:
        print("[ (", end="")
        cnt = 0
        for r in row:
            if cnt == k2_:
                print(") , (", end="")
                cnt = 0
            elif cnt:
                print(", ", end="")
            print(r, end=" ")
            cnt += 1
        print(") ]")
    table = PrettyTable()
    table.field_names = ["Parameters", "Value"]
    table.add_row(["v1", v1])
    table.add_row(["v2", v2])
    table.add_row(["b1", b1])
    table.add_row(["b2", b2])
    table.add_row(["r1", r1])
    table.add_row(["r2", r2])
    table.add_row(["k1", k1])
    table.add_row(["k2", k2])
    table.add_row(["lambda111", lambda111])
    table.add_row(["lambda112", lambda112])
    table.add_row(["lambda122", lambda122])
    table.add_row(["lambda211", lambda211])
    table.add_row(["lambda212", lambda212])
    table.add_row(["lambda222", lambda222])
    print(table)

    nbbpb = np.array(nbbpb)
    e1 = efficiency_merging.get_efficiency(v1, v2, nbbpb)
    print("Block Efficiency for NBBPB: ", e1)
    nbbpb_sub = []
    for i in range(0, nbbpb.shape[1], k2):
        for j in range(nbbpb.shape[0]):
            nbbpb_sub.append(nbbpb[j][i:i+k2])
    nbbpb_sub = np.array(nbbpb_sub)
    e2 = efficiency_merging.get_efficiency(v1, v2, nbbpb_sub,)
    print("Sub-Block Efficiency for NBBPB: ", e2)


file_path = input("Enter the file path: ")


def is_valid_file(file_path):
    return os.path.exists(file_path)


if is_valid_file(file_path):
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    sub_block_size = int(input("Enter the sub block size: "))
    alpha = int(input("Enter the value of alpha: "))
    control_treatments = int(input("Enter the number of control treatments: "))
    method2(data, sub_block_size, alpha,  control_treatments)
else:
    print("File path is not valid.")
