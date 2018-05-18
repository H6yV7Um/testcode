from __future__ import print_function
import itertools
from itertools import product


def perm(seq): 
    #长度10的列表全排列递归版本要慢于perm3循环版本10+倍：10s:0.7s
    begin=0
    end = len(seq)
    #递归终止条件，当remain seq只剩一个元素时则停止，因为无法swap了
    if begin >= end:  
        yield seq
    else:  
        for num in range(begin,end): 
            #序列中的元素依次作为头牌元素，然后递归余下元素
            seq[num],seq[begin]=seq[begin],seq[num]  
            yield from perm(seq, begin+1, end)  
            #还原seq，便于下次循环递归
            seq[num],seq[begin]=seq[begin],seq[num]  

def perm2(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

def perm3(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    #[0,1,2,3]
    indices = list(range(n))
    #n=r [4,3,2,1]
    cycles = list(range(n, n-r, -1))    #不同的实现无明显性能差异，尽量使用易于理解的版本
    #首次返回与原序列顺序一致的元组
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):    #[3,2,1,0]
            cycles[i] -= 1   
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]   #1
                #[0,1,2,3] -> [0,1,3,2]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def perm_count(n):
    count = 1
    for i in range(n,0,-1):
        count *= i
    return count

n = list(range(10))

import time
start = time.time()
s = perm3(n)
# s = itertools.permutations(n)
# s = perm3(n)
num = 0
for i in s:
    # print(i)
    num+=1
print(num) 
elapsed = int((time.time() - start)*1000)  
print("elapsed:", elapsed)

'''
机器8核2.1GHz的CentOS  长度为11的列表全排列39916800项 平均耗时
java：660ms左右
这还是用的标准库的全排列算法，自定义的递归方式要慢10倍
cpython：8300ms左右
pypy：2500ms左右
'''


