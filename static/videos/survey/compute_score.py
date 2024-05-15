import glob
from ipdb import set_trace

import os
import random
import copy

import csv

cadidate = ['avbeat', 'baseline', 'cmt','nce', 'VidCaption']

my_res = {
    'avbeat': 0,
    'baseline': 0,
    'cmt': 0,
    'nce': 0,
    'VidCaption':0
}

## cmt check: 1-3 2-3 3-1
ordder = [[1, 4, 2, 0, 3], [1, 4, 2, 0, 3], [2, 1, 4, 0, 3], [1, 3, 4, 0, 2], [2, 4, 0, 1, 3], [1, 3, 2, 4, 0], [0, 1, 2, 4, 3], [0, 2, 3, 1, 4], [0, 3, 1, 2, 4], [2, 0, 4, 1, 3], [0, 1, 3, 2, 4], [2, 4, 1, 0, 3], [4, 3, 2, 1, 0], [3, 2, 1, 4, 0], [3, 4, 1, 0, 2]]

with open('Overall_v1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        count = 0
        for results in row:
            if count !=0:
                tmp_res_id = int(row[results].split('/')[-1][-5])-1
                # print(tmp_res_id)
                # print(ordder[count-1])
                # print(cadidate[ordder[count-1][tmp_res_id]])
                my_res[cadidate[ordder[count-1][tmp_res_id]]] +=1
                
            count +=1

print("overall:", my_res)


my_res_2 = {
    'avbeat': 0,
    'baseline': 0,
    'cmt': 0,
    'nce': 0,
    'VidCaption':0
}

with open('Relevance_v1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        count = 0
        for results in row:
            if count !=0:
                tmp_res_id = int(row[results].split('/')[-1][-5])-1
                # print(tmp_res_id)
                # print(ordder[count-1])
                # print(cadidate[ordder[count-1][tmp_res_id]])
                my_res_2[cadidate[ordder[count-1][tmp_res_id]]] +=1
            count +=1
print('Relevance:',my_res_2)