#这个数列从第3项开始，每一项都等于前两项之和。
def fib1(n, f=1, s=1, cache={}):
    '''递归版'''
    import sys
    sys.setrecursionlimit(9999)
    result = cache.get(n)
    if result is None:
        if n == 1:
            result = f
        if n == 2:
            result = s
        elif n > 2:
            result = fib1(n-2) + fib1(n-1)
        cache[n] = result
    return result

def fib2(n, result=[1, 1]):
    '''循环版'''
    if n == 1:
        return result[0]
    if n == 2:
        return result[1]
    for i in range(2, n):
        result.append(result[i-2] + result[i-1])
    return result[n-1]

from functools import lru_cache

@lru_cache(maxsize=1024)
def fib3(n, f=1, s=1):
    if n == 1:
        return f
    if n == 2:
        return s
    if n > 2:
        return fib3(n-2) + fib3(n-1)

class Fib:
    
    @classmethod
    @lru_cache(maxsize=1024)
    def fib3(cls, n, f=1, s=1):
        if n == 1:
            return f
        if n == 2:
            return s
        if n > 2:
            return cls.fib3(n-2) + cls.fib3(n-1)

if __name__ == '__main__':
    from classic_sort import timer
    timer(fib2)(1000)
    timer(fib1)(1000)
    timer(Fib().fib3)(1000)
    print(Fib.fib3.cache_info())
