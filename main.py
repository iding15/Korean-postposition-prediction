import time
from typing import List
from pred import predict_with_decision_tree
from preprocessing import Target, NounData
from noun_data import get_noun_data
import pandas as pd
from functools import reduce


noun_data = get_noun_data()['data']

en = Target(noun_data, 'en').parse()
ig = Target(noun_data, 'ig').parse()
er = Target(noun_data, 'er').parse()

# print(en)
# print(ig)
# print(er)

# 최적 weight 찾기
start_time = time.time()
LOG_CHECK_TIME = 10

weights = []
for x in range(11):
    for y in range(11):
        for z in range(11):
            weights.append([x, y, z])

assert len(weights) == 11*11*11, 'weight length is unexpected, get' + len(weights)
print('get accuracy scores now ...')

def list_to_str(l: List[str]):
    start_brace = '['
    fin_brace = ']'
    return start_brace+', '.join(list(map(str, l)))+fin_brace

prev_time = start_time
score_info = []
for i, w in enumerate(weights):
    score_info.append((list_to_str(w), predict_with_decision_tree(NounData(noun_data, w).parse(), en)))
    now_time = time.time()
    elapsed_time = now_time-prev_time
    if elapsed_time > LOG_CHECK_TIME:
        print(f'{now_time-start_time}s: {i+1}th prediction is processed.')
        prev_time = now_time

print('get optimized score info success!!')

def get_max(info1, info2):
    a1 = info1[1]
    a2 = info2[1]
    return info1 if a1>a2 else info2

result = reduce(get_max, score_info)
print(result)
