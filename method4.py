import csv
from prettytable import PrettyTable
import efficiency_merging
import numpy as np
import os


def get_bbpb_params(design):
    v = 0
    for row in design:
        for cur in row:
            if cur > v:
                v = cur
    freq = {}
    for row in design:
        for cur in row:
            if cur in freq:
                freq[cur] += 1
            else:
                freq[cur] = 1
    freq_set = set()
    for key in freq:
        freq_set.add(freq[key])
    if len(freq_set) != 2:
        print("Error: The design is not a BBPB")
        exit(1)
    for i in range(1, v+1):
        if freq[i] != freq[1]:
            v1 = i - 1
            v2 = v - v1
            break

    b = len(design)
    r1 = 0
    r2 = 0
    for row in design:
        for cur in row:
            if cur == 1:
                r1 += 1
            if cur == v:
                r2 += 1
    k = len(design[0])
    lambda11 = 0
    lambda12 = 0
    lambda22 = 0
    for row in design:
        if 1 in row and 2 in row and v1 > 1:
            lambda11 += 1
        if 1 in row and v in row:
            lambda12 += 1
        if v-1 in row and v in row and v2 > 1:
            lambda22 += 1
    return [v1, v2, b, r1, r2, k, lambda11, lambda12, lambda22]


def get_nbib_params(design, sub_block_size):
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


def method4(bbpb_design, nbib_design, nbib_sub_block_size):
    if (not isinstance(bbpb_design, list)):
        print("Error: bbpb_design must be a list.")
        return -1
    for i in range(len(bbpb_design)):
        for j in range(len(bbpb_design[i])):
            bbpb_design[i][j] = int(bbpb_design[i][j])
    try:
        [v1_, v2_, b_,  r1_, r2_, k_, lambda11_, lambda12_,
            lambda22_] = get_bbpb_params(bbpb_design)
    except:
        print("Error: unable to get parameters from the bbpb_design.")
        return -1

    if (v1_ <= 0 or v2_ <= 0 or b_ <= 0 or r1_ <= 0 or r2_ <= 0 or k_ <= 0 or lambda11_ <= 0 or lambda12_ <= 0 or lambda22_ <= 0):
        print("Error: all parameters must be positive integers[BBPB Design].")
        return -1

    if (v1_*r1_ + v2_*r2_ != b_*k_):
        print("Error: v1*r1 + v2*r2 = b*k should be satisfied[BBPB Design].")
        return -1
    if (r1_ * (k_ - 1) != lambda11_ * (v1_ - 1) + lambda12_ * v2_):
        print(
            "Error: r1*(k-1) = lambda11*(v1-1) + lambda12*v2 should be satisfied[BBPB Design].")
        return -1
    if (r2_ * (k_ - 1) != lambda22_ * (v2_ - 1) + lambda12_ * v1_):
        print(
            "Error: r2*(k-1) = lambda22*(v2-1) + lambda12*v1 should be satisfied[BBPB Design].")
        return -1
    if (lambda12_ > r1_) or (lambda12_ > r2_) or (lambda11_ > r1_) or (lambda22_ > r2_):
        print(
            "Error: lambda values should be less than r values[BBPB Design].")
        return -1
    if (r1_*r2_ < lambda12_ * b_):
        print("Error: r1*r2 should be greater than lambda12*b[BBPB Design].")
        return -1

    if (not isinstance(nbib_design, list)):
        print("Error: nbib_design must be a list[BBPB Design].")
        return -1
    for i in range(len(nbib_design)):
        for j in range(len(nbib_design[i])):
            nbib_design[i][j] = int(nbib_design[i][j])
    try:
        [v__, b1__, b2__, r__, k1__, k2__, lambda1__, lambda2__] = get_nbib_params(
            nbib_design, nbib_sub_block_size)
    except:
        print("Error: unable to get parameters from the nbib_design.")
        return -1

    if (v__ <= 0 or b1__ <= 0 or b2__ <= 0 or r__ <= 0 or k1__ <= 0 or k2__ <= 0 or lambda1__ <= 0 or lambda2__ <= 0):
        print("Error: all parameters must be positive integers[NBIB Design].")
        return -1

    q__ = b2__/b1__
    q__ = int(q__)
    if (v__*r__ != b1__*k1__ or b1__*k1__ != b2__*k2__ or b2__*k2__ != q__*b1__*k2__):
        print(
            "Error: v*r = b1*k1 = q*b1*k2 = b2*k2 should be satisfied[NBIB Design].")
        return -1
    if ((v__-1)*lambda1__ != (k1__-1)*r__):
        print(
            "Error: (v-1)*lambda1 = (k1-1)*r should be satisfied[NBIB Design].")
        return -1

    if ((v__-1)*lambda2__ != (k2__-1)*r__):
        print(
            "Error: (v-1)*lambda2 = (k2-1)*r should be satisfied[NBIB Design].")
        return -1

    if ((v__-1)*(lambda1__ - q__*lambda2__) != (q__-1)*r__):
        print(
            "Error: (v-1)*(lambda1 - q*lambda2) = (q-1)*r should be satisfied[NBIB Design].")
        return -1

    if (v__ != k_):
        print(
            "Error: v of NBIBD should be equal to k of BBPB for valid construction[NBIB Design].")
        return -1

    nbbpb = []
    for row in bbpb_design:
        mapping = {}
        for i in range(len(row)):
            mapping[i+1] = row[i]
        print(mapping)
        for r in nbib_design:
            new_row = []
            for i in range(len(r)):
                new_row.append(mapping[r[i]])
            nbbpb.append(new_row)
    v1 = v1_
    v2 = v2_
    b1 = b_ * b1__
    b2 = b_ * b2__
    r1 = r1_ * r__
    r2 = r2_ * r__
    k1 = k1__
    k2 = k2__
    lambda111 = int(lambda11_ * lambda1__)
    lambda112 = int(lambda12_ * lambda1__)
    lambda122 = int(lambda22_ * lambda1__)
    lambda211 = int(lambda11_ * lambda2__)
    lambda212 = int(lambda12_ * lambda2__)
    lambda222 = int(lambda22_ * lambda2__)
    table = PrettyTable()

    print("NBBPB Design: ")
    for row in nbbpb:
        print("[ (", end="")
        cnt = 0
        for r in row:
            if cnt == k2:
                print(") , (", end="")
                cnt = 0
            elif cnt:
                print(", ", end="")
            print(r, end=" ")
            cnt += 1
        print(") ]")

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
    e2 = efficiency_merging.get_efficiency(v1, v2, nbbpb_sub)
    print("Sub-Block Efficiency for NBBPB: ", e2)


bbpb_file_path = input("Enter the BBPB design file path: ")
nbib_file_path = input("Enter the NBIB design file path: ")


def is_valid_file(file_path):
    return os.path.exists(file_path)


if is_valid_file(bbpb_file_path) and is_valid_file(nbib_file_path):
    with open(bbpb_file_path, newline='') as f:
        reader = csv.reader(f)
        bbpb_design = list(reader)
    with open(nbib_file_path, newline='') as f:
        reader = csv.reader(f)
        nbib_design = list(reader)
    nbib_sub_block_size = int(input("Enter the size of sub block for NBIB: "))
    method4(bbpb_design, nbib_design, nbib_sub_block_size)
else:
    print("File path is not valid.")
