#!/bin/python3

import math
import os
import random
import re
import sys

# def list_comp():
#     x = int( raw_input())
#     y = int( raw_input())
#     n = int( raw_input())
#     print([[i, j] for i in range( x + 1) for j in range( y + 1)
#           if ( ( i + j ) != n )])

# # Complete the solve function below.
# def solve(a, b):
#     # alice = 0
#     # bob = 0
#     for alpha, bravo in zip(a,b):
#         alice = 0
#         bob = 0
#         if alpha > bravo:
#             alice +=1
#         if bravo < alpha:
#             bob +=1
#         else:
#             continue
#         return alice, bob
#     # alice = [alpha > bravo for alpha, bravo in zip(a,b)]
#     # bob = [bravo > alpha for alpha, bravo in zip(a,b)]
#     # if alpha > bravo
#     # print(alice)
#     # print(bob)
#
# if __name__ == '__main__':
# #     fptr = open(os.environ['OUTPUT_PATH'], 'w')
#
#     a = list(map(int, input().rstrip().split()))
#
#     b = list(map(int, input().rstrip().split()))
#
#     result = solve(a, b)
#
# #    fptr.write(' '.join(map(str, result)))
# #    fptr.write('\n')
#
# #    fptr.close()
#
#     print(result)
