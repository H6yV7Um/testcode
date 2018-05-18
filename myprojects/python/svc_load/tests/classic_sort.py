 
from itertools import chain
from random import shuffle 
from time import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        start = time()
        result = func(*args, **kwds)
        elapsed = int((time() - start)*1000)
        print("{} elapsed: {}ms".format(func.__name__, elapsed))
        return result
    return wrapper

'''

'''

def simple_sort(l):
    l_len = len(l)
    for i in range(l_len):
        min_index = i
        for j in range(i+1, l_len):
            if l[min_index] >= l[j]:
                min_index = j
        #最小值的位置有变化时才做交换操作
        if min_index != i:
            l[i], l[min_index] = l[min_index], l[i]
    return l
'''
由示例可见，简单排序也是双层循环，普遍情况下需要比较n^2次，所以其时间复杂度为O(n^2)，但是交换操作次数最多为n次，这一点是要强于冒泡排序的。
'''

#关于算法稳定性：搜索关键词“排序算法稳定性”

'''
归并排序算法是采用分治法的一个非常典型的应用，何谓分治，简单来讲就是化整为零，将大块拆成多个小块，分而治之。
算法原理：先把序列划分为n个子序列，然后对每个子序列排序，最后将子序列合并得到一个有序的最终序列。
归并排序的算法我们通常用递归实现，先把待排序区间以中点二分，接着把左边子区间排序，再把右边子区间排序，最后把左区间和右区间用一次归并操作合并成有序的区间。
'''
def merge_sort(lists):
    if len(lists) <= 1:
        return lists
    num = int( len(lists) / 2 )
    #对左右子区间通过递归调用，使左右子区间都有序
    left = merge_sort(lists[:num])
    right = merge_sort(lists[num:])
    #merge函数用来将左右区间合并为最终排好序的结果序列
    def merge():
        r, l=0, 0
        result=[]
        while l<len(left) and r<len(right):
            if left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        #通过上边的比较，最终left[l:]和right[r:]必有一个为空，剩下不为空的区间则包含了最后一部分数值较大的有序序列，直接追加到结果序列之后即可
        result += left[l:]
        result += right[r:]
        return result
    return merge()
'''
通过例子可以看到，如果序列的长度为n=8，拆分为子序列要经过8/2,4/2,2/2这三步，而每个子序列都要经过merge_sort，也就是要经过log8=3次，每次归并要经过的最大比较次数为n，则总计要比较nlogn次，所以归并排序的时间复杂度为O(nlogn)。归并排序不是就地排序即不是在原序列上进行的，而是最终产出一个长度为n的新序列，所以其空间复杂度为O(n)。归并排序比较占用内存，但却是一种效率高且稳定的算法，效率仅次于快速排序，稍后列举完几个排序算法之后会给出实际的对比数据供参考。
'''

'''
快速排序也是分治法的应用算法之一。其原理是：首先选中一个基准值，一般为中间值，然后序列中的其他值与基准值做比较，小于基准值的放入一个数组A中，大于基准值的放入另一个数组B中，只要数组A和数组B是有序的，那么A+基准值+B则为最终的排好序的结果。
'''
def quick_sort(seq):
    if len(seq) < 2:
        return seq
    small_list = []
    big_list = []
    #median为基准值
    median_index = int(len(seq)/2)
    median = seq[median_index]
    front = seq[:median_index]
    end = seq[median_index+1:]
    for num in chain(front, end):
        if num > median:
            big_list.append(num)
        else:
            small_list.append(num)
    return quick_sort(small_list) + [median] + quick_sort(big_list)
'''
从示例中可以看到，快速排序也是需要不断的二等分，所以也需要递归logn个子序列，跟归并算法有点相似，但是由于每次都会抽取一个基准值，所以每个子序列需要比较n-1次(n表示子序列长度，时间复杂度计算中不作过细区分，而且忽视常量)，所以快速排序的时间复杂度也是O(nlogn)，但是效率是高于归并排序的，因为n值较小。
'''

def bubble_sort1(l, p=None):
    l_len = len(l) if p is None else p
    if l_len <=1:
        return
    indies = range(l_len)
    for i in indies:
        if i == l_len-1:
            break
        if l[i] > l[i+1]:
            l[i], l[i+1] = l[i+1], l[i]
    bubble_sort(l, l_len-1)
'''
冒泡排序原理：从第一个元素开始，依次比较相邻的两个元素，如果他们的顺序错误就把他们交换过来。对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。经过这样的一遍比较，最后的元素应该会是最大的数。针对所有的元素重复以上的步骤，除了最后一个。持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较，也就是排序完成了。
这个算法的名字由来是因为越大的元素会经由交换慢慢“浮”到数列的顶端，故名“冒泡排序”。
'''
def bubble_sort(l):
    l_len = len(l)
    while l_len > 1:
        index = range(l_len-1)
        for i in index:
            if l[i] > l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]
        l_len -= 1

def bubble_sort3(l):
    for i in range(len(l)-1):   
        for j in range(len(l)-i-1):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
    return l
'''
通过示例可以看到，要经过两层循环的比较，所以冒泡排序的时间复杂度是O(n^2)。冒泡排序是就地排序，所以没有额外空间的消耗。
'''

'''
直接插入排序算法把要排序的数组分成两部分：第一部分包含了已排好序的数组A，而第二部分包含了无序的待插入元素的数组B。每次B中取一个元素，从右向左依次与数组A中的元素比较，直到找到合适位置，然后将该元素插入到A中，使A继续保持有序，如此往复，直到整个数组排序完成。
'''
def insert_sort(l):
    #开始时假设l[0:1]就是已排好序的数组A，l[1:]为待排序的数组B
    #所以索引从1开始，遍历B，不断插入到数组A中
    for i in range(1, len(l)):
        #待插入的元素
        insert = l[i]   
        #如果已排好序数组A的最右边的元素大于待插入元素
        if l[i-1] > l[i]: 
            #index用来记录待插入元素的位置
            index = i 
            #从右向左依次与待插入元素做比较，直到找到合适的位置
            while index > 0 and l[index - 1] > insert:
                # 把已经排序好的元素后移一位，留下需要插入的位置
                l[index] = l[index - 1]     
                index -= 1
            l[index] = insert # 把需要排序的元素，插入到指定位置
    return l

'''
示例中可以看到也是两层循环，但是有条件限制，如果序列本身是有序的则只需要遍历n次，时间复杂度则为O(n)；如果是无序的，并且条件l[i-1] > l[i]每次都成立的话，当然这是最坏的情况，所以其最坏时间复杂度为O(n^2)
'''

'''
评价排序算法优劣的标准主要是两条：一是算法的运算量，这主要是通过记录的比较次数和移动次数来反应；另一个是执行算法所需要的附加存储单元的的多少。
'''

if __name__ == '__main__':
    l = list(range(10000000))
    sort_funcs = [func for name, func in globals().items() if name.endswith("_sort")]
    for func in sort_funcs:
        shuffle(l)
        #这里提醒一下，不要将timer装饰器通过语法糖@绑定到函数上，因为递归的关系，你懂得
        timer(func)(l)


