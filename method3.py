import csv
from prettytable import PrettyTable
import efficiency_non_merging
import numpy as np
import os


def get_params(design):
    v = 0
    for row in design:
        for cur in row:
            if cur > v:
                v = cur
    b = len(design)
    r = 0
    for row in design:
        for cur in row:
            if cur == 1:
                r += 1
    k = len(design[0])
    lambda_ = ((k-1)*r)/(v-1)
    return [v, b,  r, k, lambda_]


def method3(bib_design, v2):
    if (not isinstance(bib_design, list)):
        print("Error: bib_design must be a list.")
        return -1
    for i in range(len(bib_design)):
        for j in range(len(bib_design[i])):
            bib_design[i][j] = int(bib_design[i][j])
    try:
        [v_, b_,  r_, k_, lambda_] = get_params(
            bib_design)
    except:
        print("Error: unable to get parameters from the bib_design.")
        return -1

    if (v_ <= 0 or b_ <= 0 or r_ <= 0 or k_ <= 0 or lambda_ <= 0):
        print("Error: all parameters must be positive integers.")
        return -1

    if (v_*r_ != b_*k_):
        print("Error: v*r = b*k should be satisfied.")
        return -1

    if ((v_-1)*lambda_ != (k_-1)*r_):
        print("Error: (v-1)*lambda = (k-1)*r should be satisfied.")
        return -1

    if (v_ > b_):
        print("Error: v <= b should be satisfied.")
        return -1

    if (k_ != 3):
        print("Error: k must be 3 for construction of NBBPB.")
        return -1

    nbbpb = []
    control_treatments = []
    for i in range(v_+1, v_+1+v2):
        control_treatments.append(i)
    for row in bib_design:
        r = []
        for value in row:
            r.append(value)
        tmp = []
        tmp.append(r[0])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        tmp.append(r[1])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        nbbpb.append(tmp)
        tmp = []
        tmp.append(r[0])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        tmp.append(r[2])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        nbbpb.append(tmp)
        tmp = []
        tmp.append(r[1])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        tmp.append(r[2])
        for i in range(0, len(control_treatments)):
            tmp.append(control_treatments[i])
        nbbpb.append(tmp)

    v1 = v_
    b1 = b_*3
    b2 = b_ * 6
    r1 = r_*2
    r2 = b_*6
    k1 = k_*2
    k2 = k_
    lambda111 = int(lambda_)
    lambda112 = 4*r_
    lambda122 = 12 * b_
    lambda211 = 0
    lambda212 = 2*r_
    lambda222 = 6*b_
    table = PrettyTable()

    print("NBBPB Design: ")
    for row in nbbpb:
        print("[ (", end="")
        cnt = 0
        for r in row:
            if cnt == 1 + v2:
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
    e1 = efficiency_non_merging.get_efficiency(nbbpb, v1, v2, b1, k1)
    print("Block Efficiency for NBBPB: ", e1)
    nbbpb_sub = []
    for i in range(0, nbbpb.shape[1], k2):
        for j in range(nbbpb.shape[0]):
            nbbpb_sub.append(nbbpb[j][i:i+k2])
    nbbpb_sub = np.array(nbbpb_sub)
    e2 = efficiency_non_merging.get_efficiency(nbbpb_sub, v1, v2, b2, k2)
    print("Sub-Block Efficiency for NBBPB: ", e2)


file_path = input("Enter the file path: ")


def is_valid_file(file_path):
    return os.path.exists(file_path)


if is_valid_file(file_path):
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    control_treatments = int(input("Enter the number of control treatments: "))
    method3(data, control_treatments)
else:
    print("File path is not valid.")
