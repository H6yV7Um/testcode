'''
给你的代码加点buff
python中将一个可调用对象A作为参数传给另一个可调用对象B，经过处理返回原来的A或是加了buff的A，这时将可调用对象B称为一个装饰器，可以是装饰器函数或装饰器类。
'''

'''
装饰器有两种使用方式:利用语法糖@,也就是上边例子所示的方式，另一种是比较原始的无糖型方式

'''
'''
一、利用语法糖@将装饰器绑定到目标上，装饰器的绝大部分使用都是利用这种方式
'''

from functools import wraps

def simple_dec(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        print("Decorated function:{}".format(func.__name__))
        return func(*args, **kwds)
    return wrapper

@simple_dec
def simple_func():
    pass
print("I am actually wrapper:", simple_func)
print("I am real simple_func:", simple_func.__wrapped__)
simple_func()

#利用装饰器为函数添加额外属性
def parameter_dec(**kwds):
    def decorator(func):
        for name, value in kwds.items():
            setattr(func, name, value)
        @wraps(func)
        def wrapper(*args):
            return func(*args)
        return wrapper
    return decorator

@parameter_dec(hello="world")
def parameter_func(n):
    print("I am parameter_func")

print(parameter_func.__wrapped__.hello)
'''
用过装饰器的人应该都知道wraps，它可以保留源函数的某些特殊属性，比如func.__name__，如果不使用wraps，那么func.__name__就会返回wrapper。其实wraps装饰器就是进行了一些复制操作，把被装饰的源函数的某些属性复制到wrapper函数中，特殊属性包括：'__module__', '__name__', '__qualname__', '__doc__','__annotations__','__dict__'。并给wrapper添加了个特殊属性__wrapped__，值为func函数，算是一个特殊接口用来访问原始的函数。所以尽管使用了wraps，访问func.__name__其实还是访问了wrapper.__name__
'''

'''
二、无糖的执行方式
我们以例子1-1来说明这种执行方式，当调用被装饰的函数:simple_func()，其实就相当于simple_dec(simple_func)()，很明显分为两步调用，先以simple_func作为参数调用simple_dec，返回另一个函数然后再次调用。这种方式其实就是装饰器的本来面目，比较丑陋晦涩难懂。再回看例子1-2，调用被装饰的函数parameter_func就相当于parameter_dec(hello="world")(func)(n)，这种方式简直了，还没凤姐直观呢。而语法糖@正是为了解决这种丑陋的调用方式而产生的，让代码变得更加正解易懂。那既然无糖的方式这么low直接抛弃掉，只用语法糖的方式不得了。nonono，low有low的好处，糖分低不容易得糖尿病。


for method in methods:
    decorator(method)(args)
'''
#装饰器执行顺序
def dec1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('I am dec1')
        return func(4)
    return wrapper

def dec2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('I am dec2')
        return func(3)
    return wrapper

@dec2
@dec1
def func(num):
    print('I am func, my arg:', num)

func(999)

def free_func(num):
    print('I am free_func, my arg:', num)

'''
提供一些基于装饰器的使用示例，有些是标准库提供的，有些是自定义的
熟悉python的人都应该知道property装饰器，是基于C实现的。下边的例子提供了python版的实现，笔者做了点小改进，增加了类型校验，比较糙，主要看原理。
'''

class myproperty:
    def __init__(self, func):
        self._getter = func
    
    def __get__(self, obj, cls):
        if not obj:
            return self
        result = self._getter(obj)
        return result
    
    def __set__(self, obj, value):
        if value.__class__ != self._cls:
            raise TypeError("The type of value must be {}".format(self._cls))
        self._setter(obj, value)
  
    def setter(self, cls):
        self._cls = cls
        def wrapper(func):
            if func.__name__ != self._getter.__name__:
                raise NameError("The name of setter must be same with getter's")
            self._setter = func
            return self
        return wrapper
        
class Test:
    def __init__(self):
        self._value = None

    @myproperty
    def value(self):
        return self._value

    @value.setter(int)
    def value(self, value):
        self._value = value

t = Test()
t.value = 666
print(t._value)
# t.value = "hello world"

'''
这个例子中myproperty装饰器的作用相当于这个表达式：t.value = myproperty(value),也就是将一个描述器实例赋值给t.value，这样在对t.value访问或是赋值时会先访问描述器对象(即myproperty(value))的__get__和__set__特殊方法，从而改变了该属性的访问与赋值方式。如果不了解描述器相关知识，可以先参考笔者的另一篇文章，相信会让你有所顿悟。这个例子的核心技术还是描述器居多，但是相比于直接将描述器实例赋值给属性的方式，通过装饰器让描述器的使用方法变得更加优雅，这也是装饰器的一大优点。
'''

'''
利用标准库中的singledispatch，根据参数类型实现函数重载
'''
from functools import singledispatch

@singledispatch
def fun(arg, verbose=True):
    print(arg)

@fun.register(int)
def _(arg):
    print("int arg:", arg)

@fun.register(list)
def _(arg):
    print("list arg:", arg)

fun(123)
fun([1,2,3,4])
'''
输出：
int arg: 123
list arg: [1, 2, 3, 4]
熟悉java的人应该都知道，java中的方法重载很方便，因为它是强类型语言，相同的方法名不同的参数类型该方法的签名就不同。python是弱类型语言，通过对参数类型判断也可以实现重载，但是远不如通过装饰器来的优雅，代码风格上有点类似java，不同类型的参数单独定义其方法，使代码更加清晰易懂。
'''

'''
添加lru_cache示例
'''
from functools import lru_cache

@lru_cache(maxsize=1024)
def fib1(n, f=1, s=1):
    if n == 1:
        return f
    if n == 2:
        return s
    if n > 2:
        return fib1(n-2) + fib1(n-1)

def fib2(n, f=1, s=1):
    if n == 1:
        return f
    if n == 2:
        return s
    if n > 2:
        return fib2(n-2) + fib2(n-1)

from classic_sort import timer
timer(fib1)(100)
timer(fib2)(40)
'''
添加单例类装饰器示例
'''
def signleton(cls):
    cache = None
    def wrapper(*args, **kwds):
        nonlocal cache
        if cache is None:
            cache = cls(*args, **kwds)
        return cache
    return wrapper

@signleton
class Test:
    pass

t = Test()
a = Test()
print("t is a:", t is a)

'''
通过上面的例子可以看到，装饰器可以给被装饰对象增加额外功能，使之成为增强版，就像游戏中给角色增加了buff一样。这里再顺便提下另一个与装饰器有关的概念：AOP面向切面编程。关于AOP编程网上有很多专业的介绍，个人理解其本质就是在不修改核心代码的前提下为该核心代码增加特定功能的特殊编程方法，python中的装饰器其实只是AOP面向切面编程的一种实现方式。在很多框架中比如Django和spring，都提供了基于AOP的功能，使开发更加简单并且极大提高开发效率，比如请求缓存，通用异常处理，自定义权限验证，日志划分处理等。
'''


if __name__ == '__main__':
    func(1)
    dec2(dec1(free_func))(5)

    print(parameter_func.__wrapped__)
    # print(dir(parameter_func))

'''
https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
Reference Documents
class decorator
https://www.python.org/dev/peps/pep-3129/

decorator for functions and methods
https://www.python.org/dev/peps/pep-0318/

shops:
{"code":0,"data":{"id":3,"name":"XX日用品专营店","categoryId":19,"categoryName":"日用百货","describe":"XX首家大型日用品专营店，从事日用品经营达20余年，经营各类纸品、卫生巾、各类生活清洁用品等","address":"XXX路12号","phone":"13700000000","expiredTime":null,"createTime":"2017-08-28 16:48:25","updateTime":"2017-11-20 14:13:10","longitude":"119.5438027382","latitude":"26.1974470461","avatar":"http://img.leshare.shop/seller/shulanriyongpin.png","autoOrder":1,"leArea":350500,"offPay":1,"detailAddress":null,"inShop":0,"supportMember":1,"isDelete":0,"images":[]}}

"goodsSkuInfo":{"prop1":"规格","value1":"中杯,大杯","prop2":null,"value2":null,"prop3":null,"value3":null,"goodsSkuDetails":[{"sku":"中杯","goodsSkuDetailBase":{"price":0.01,"imageUrl":"http://img.leshare.shop/FnhRZF-MCHfl8GPZEfVTPZkQuV56"}},{"sku":"大杯","goodsSkuDetailBase":{"price":12,"imageUrl":"http://img.leshare.shop/FnhRZF-MCHfl8GPZEfVTPZkQuV56"}}]}

"goodsStocks":[{"goodsId":241,"sku":"中杯","stock":96},{"goodsId":241,"sku":"大杯","stock":70}]

inner_category:
"data":[{"id":559,"pid":0,"name":"推荐","shopId":6,"seq":1,"createTime":"2018-02-07 09:46:36","updateTime":"2018-02-07 09:46:36","isDelete":0,"isShow":0,"type":"RECOMMEND"},{"id":55,"pid":0,"name":"配料区","shopId":6,"seq":2,"createTime":"2017-11-02 10:52:44","updateTime":"2017-11-02 10:52:44","isDelete":0,"isShow":1,"type":"CUSTOM"}

coupons:
status:EXPIRED NEVER_USED USED
{"code":0,"data":[{"id":0,"name":"见面礼","type":"CASH","price":1,"limitPrice":100,"shopId":3,"beginTime":"2017-08-29 00:00:00","dueTime":"2017-09-30 00:00:00","stock":1,"perLimit":1,"suitLimit":0,"createTime":"2017-09-29 20:44:56","isCampaign":0,"campaignImg":null,"campaignScene":0,"isPlatform":0,"supportType":0,"isSelfUse":0,"isPresent":0,"presentFee":0,"isShow":0,"isShowHome":0,"desc":null,"goodsIdList":[],"couponCustomerCount":{"couponId":8,"acceptCount":3,"usedCount":0},"sendNow":false},{"id":0,"name":"大特惠","type":"CASH","price":10,"limitPrice":100,"shopId":3,"beginTime":"2017-11-19 00:00:00","dueTime":"2017-12-19 00:00:00","stock":1000,"perLimit":1,"suitLimit":0,"createTime":"2017-11-19 19:49:18","isCampaign":0,"campaignImg":null,"campaignScene":0,"isPlatform":0,"supportType":0,"isSelfUse":1,"isPresent":0,"presentFee":0,"isShow":0,"isShowHome":0,"desc":null,"goodsIdList":[],"couponCustomerCount":{"couponId":13,"acceptCount":1,"usedCount":0},"sendNow":false},{"id":0,"name":"小特惠","type":"CASH","price":5,"limitPrice":10,"shopId":3,"beginTime":"2017-11-19 00:00:00","dueTime":"2017-12-19 00:00:00","stock":100,"perLimit":1,"suitLimit":0,"createTime":"2017-11-19 19:49:30","isCampaign":0,"campaignImg":null,"campaignScene":0,"isPlatform":0,"supportType":0,"isSelfUse":1,"isPresent":0,"presentFee":0,"isShow":0,"isShowHome":0,"desc":null,"goodsIdList":[],"couponCustomerCount":{"couponId":14,"acceptCount":1,"usedCount":0},"sendNow":false},{"id":0,"name":"中特惠","type":"CASH","price":8,"limitPrice":50,"shopId":3,"beginTime":"2017-11-19 00:00:00","dueTime":"2017-12-19 00:00:00","stock":100,"perLimit":1,"suitLimit":0,"createTime":"2017-11-19 19:49:41","isCampaign":0,"campaignImg":null,"campaignScene":0,"isPlatform":0,"supportType":0,"isSelfUse":0,"isPresent":0,"presentFee":0,"isShow":0,"isShowHome":0,"desc":null,"goodsIdList":[],"couponCustomerCount":{"couponId":15,"acceptCount":1,"usedCount":0},"sendNow":false},{"id":0,"name":"测试优惠券","type":"CASH","price":11.11,"limitPrice":100,"shopId":3,"beginTime":"2017-06-01 00:00:00","dueTime":"2017-06-30 00:00:00","stock":100,"perLimit":1,"suitLimit":0,"createTime":"2018-01-19 14:48:03","isCampaign":0,"campaignImg":null,"campaignScene":0,"isPlatform":0,"supportType":0,"isSelfUse":0,"isPresent":0,"presentFee":0,"isShow":0,"isShowHome":0,"desc":null,"goodsIdList":[],"couponCustomerCount":null,"sendNow":false}]}
wxbf987ab48beeeec3
8485eaf6074668b9223f493224e1e6e4
先把categoryId关联上数据
'''