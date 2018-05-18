'''
描述器有三个特殊方法__get__,__set__,__delete__，（此处增加方法的说明，参数等）实现任一方法的对象都可以称作
描述器对象。描述器对象又分为两种：实现了__get__和__set__的称为data descriptor
；只实现了__get__的称为non-data descriptor。python中的属性、方法、静态和类方法装饰器的实现原理都是描述器
机制，所以了解了描述器对了解python的某些底层实现是很有帮助的。

那描述器到底干了啥事儿呢？

在讨论decriptor的作用之前，先熟悉下python对象在访问属性时的查找顺序：
先调用__getattribute__特殊方法，也就是先查找对象的属性字典即a.__dict__['x'], 
然后是type(a).__dict__['x'] 然后在BaseDescclasses中查找
如果属性字典中不存在，则调用特殊方法__getattr__，前提是该对象重写了这个特殊方法。总结下就是先调用
__getattribute__方法，然后调用__getattr__方法，都没有找到没有则触发AttributeError。

敲黑板了！如果先把一个描述器对象赋值给要查找的属性，那么这个时候再访问这个属性时，其查找
顺序就会被改变了，根据descriptor的类型会进行不同的查找顺序。
如果是data descriptor，则会优先调用描述器对象的__get__方法，即a.__dict__['x'].__get__(a, type(a)),
没有查到则按对象属性的默认查找顺序继续执行；如果是non-data descriptor，则会先查找属性字典，如果没有查到
则调用a.__dict__['x'].__get__(a, type(a))，经过这两步都没有查到则再调用__getattr__，
也就是说__getattr__这个特殊方法的调用优先级是最低的。

有几点需要说明下：
1、从上边可以看到，无论是哪种描述器，在调用__get__时都得先调用a.__dict__['x']，也就是必须先调用
__getattribute__方法，可见描述器的触发都是__getattribute__。如果重写了实例对象的__getattribute__
特殊方法，则会影响描述器的自动调用，该特殊方法绝大多数情况下不要重写。
2、__get__方法中有两个参数：obj和type(obj)，如果是通过obj.x访问属性，则obj和type(obj)都会被自动传入；
如果是type(obj).x通过类访问属性,则obj为None。在实现__get__方法时需针对不同情况做相应处理。__set__和__delete
是同样的道理。
3、只要描述器对象定义了__set__和__delete__，在给属性赋值和删除时都会优先调用。
4、一个描述器对象可以将其作为属性绑定给对象，也可以像普通类那样实例化，毕竟它只是一个类

通过文字描述显得比较抽象，不容易理解，下边通过实际的例子来加深理解。

'''


class BaseDesc:
    '''用于限制属性类型'''
    def __init__(self, name):
        self.name = name
        self.value = None
        self._type = None

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if self.name in obj.__dict__:
            return obj.__dict__[self.name]
        return self.value

    def __set__(self, obj, value):
        if not isinstance(value, self._type):
            raise TypeError("The type of '{}' is not {}".format(value, self._type))
        if obj:
            obj.__dict__[self.name] = value
        self.value = value

class Integer(BaseDesc):
    def __init__(self, name):
        super().__init__(name)
        self._type = int
        
class String(BaseDesc):
    def __init__(self, name):
        super().__init__(name)
        self._type = str

class SimpleDes:
    def __init__(self):
        self._value = None

    def __set__(self, obj, value):
        self._value = value
    
    def __get__(self, obj, cls):
        return self._value

    def __delete__(self, obj):
        del self._value
        print('delete value')

class Product:
    price = Integer("price")
    name = String("name")

p = Product()
p.price = 100
p.name = 'ipad'
print(p.__dict__)

class Simple:
    anything = SimpleDes()

s = Simple()
s.anything = 'Im anything!'
print(s.anything)
print("attribute dict of Simple object:", s.__dict__)
del s.anything


import types

class FuncDes:
    '''模拟python函数或方法的实现'''
    __name__ = 'hello'

    def __init__(self, arg):
        self.arg = arg

    def __get__(self, obj, cls):
        if obj is None:
            return self
        #MethodType第一个参数必须为可调用对象
        return types.MethodType(self, obj)
    
    def __call__(self, obj=None, arg=None):
        if arg is None:
            raise SyntaxError
        if obj is None:
            print('I am a function')
        else:
            print("Im method '{}' of object '{}'".format(self.__name__, obj))
        print('my args:', arg)
        
class T:
    hello = FuncDes(arg=None)
    def __init__(self):
        self.a = 1
        self.b = 999
t = T()
print(t.hello)
t.hello('hello')

func = FuncDes(arg=None)
func(arg='world')

def test(obj, message):
    '''
    被绑定的函数，绑定到实例上后，默认第一个参数为实例对象,其实直接将实例对象传入该函数也是一样的
    只不过调用的方式变了，使代码更清晰点吧
    '''
    print("print", message)
    print(obj.a)
    print(obj.b)

t = T()
t.bound_func = types.MethodType(test, t)
print(t.bound_func("hello"))


class lazyproperty:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, cls):
        if not obj:
            return self
        result = self.func(obj)
        setattr(obj, self.func.__name__, result)
        return result
    

class Circle:
    '''
    定义了slots属性的class，其实例只能添加slots中的属性，包括构造函数中
    属性赋值和实例创建后的属性赋值，用来限制绑定额外属性很方便，不需要实现特殊
    方法增加判断操作。虽然slots主要目的是用于减少内存开支，官档也不建议作为其他
    用途，但作为一个方便的功能用用也无妨
    '''
    # __slots__ = ['radius', 'hello']

    def __init__(self, radius=123):
        self.radius = radius
        self.hello = 444

    @lazyproperty
    def area(self):
        print('compute area')
        return self.radius * 2

c = Circle(333)
print(c.area)
print(c.area)
