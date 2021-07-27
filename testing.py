#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from strassen import naive_mult
from strassen import strassen
import numpy as np
from timeit import default_timer as timer

from tqdm import tqdm
import csv

def generate_mat(start, end, dim):
    mat = [[0 for _ in range(dim)] for _ in range(dim)]

    for i in range(dim):
        for j in range(dim):
            mat[i][j] = np.random.randint(start, end)
    return mat

def sum_mat(C):
    count = 0
    for i in range(len(C)):
        for j in range(len(C)):
            count += C[i][j]
    return count


mat_size = [32, 64, 128, 256, 512, 513]

# experimental testing of crossover points
with open('crossover.csv', 'w') as f:
    def crossover():
        csv_writer = csv.writer(f)
        for i in tqdm(mat_size):
            A = generate_mat(-i, i, i)
            B = generate_mat(-i, i, i)

            for j in range(5, min(i, 60)):
                row = [0 for _ in range(3)]
                row[0] = i
                row[1] = j

                start = timer()
                strassen(A, B, i, j)
                end = timer()

                row[2] = end - start
                csv_writer.writerow(row)

    crossover()