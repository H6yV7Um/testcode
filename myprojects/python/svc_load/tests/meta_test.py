class N:
    n = 999
    def __init__(self):
        self.a = 1
        self.b = 2
    def func01(self):
        pass

    def func02(self):
        pass
n = N()
print("NameSpace of n:", dir(n))
print("n.__dict__:", n.__dict__)

#---------通过metaclass创建并自定义类-------------------
'''
metaclass是用来创建类的，所以元类中定义的所有特殊方法中的第一个参数是cls的都是代表
被创建的类对象，而且元类只能操作cls对象
'''
class BaseMeta(type):

    def __new__(cls, name, bases, nsdict):
        result = type.__new__(cls, name, bases, nsdict)
        result.members = "Hello"
        print("BaseMeta nsdict:", nsdict)
        print("dir cls:", cls.__dict__)
        return result

    def __prepare__(name, bases, **kwargs):
        '''
        首先执行该特殊方法，创建一个命名空间的映射对象
        该方法必须传入位置参数name和bases
        '''
        import collections
        print("prepare processing-name:", name)
        print("prepare processing-bases:", bases)
        nsdict = collections.OrderedDict()
        nsdict["default_ns"] = 'stop the world'
        return nsdict

    def __call__(cls):
        '''
        如果这样定义call特殊方法后，新建的类将无法实例化
        通常是在定义普通类时定义__call__(self)，这样会让该类的实例变为可调用的，
        在元类中定义该特殊方法时传入的参数是被创建的类本身cls，所以在创建类实例时会
        调用该特殊方法，也就是完全取决于传入的参数。
        '''
        print("The type of cls when call '__call__':", type(cls))
        raise RuntimeError("Can not init this class")


class A(metaclass=BaseMeta):
    def test_a(self):
        pass

class B(A):
    '''metaclass可以被继承，class B也无法被初始化'''
    def test_b(self):
        pass

print(A.members)
A.hello = 222
print("A.hello:", A.hello)
print(B.members)
print("isinstance(A, BaseMeta):", isinstance(A, BaseMeta))
print("isinstance(B, BaseMeta):", isinstance(B, BaseMeta))
print("issubclass(B, A):",issubclass(B, A))
print(A.__class__, A.__name__, B.__dict__)
# B()

#---------------通过type方法创建并自定义类----------------------
#通过type可以动态创建类，相比于通过class关键字定义一个类，提供了一种
#动态创建类的方式，可以在运行时中按需创建需要的类

print("-----------------------type---------------------------")
class Y:
    CONST = 999
    def __init__(self):
        self.m = 1
        self.n = 2
    def info(self):
        print("I'm ", type(self).__name__)
#方法的第一个参数必须为实例本身即通常所说的self
X = type('X', (Y,),{'a':1, 'func':lambda self,x,y: x+y})
class Z(X):
    pass
print("isinstance(X, type):", isinstance(X, type))
print("isinstance(Z, type):", isinstance(Z, type))
print("Y.__dict__:", Y.__dict__)
print("X.__dict__:", X.__dict__)
print('X:',X.a)
x = X()
print("x.__dict__:", x.__dict__)
x.append = 666
x.__dict__['append2'] = 777
x.append3 = lambda self: 1
print("x.__dict__:", x.__dict__)
print(x.func(1,2))
print(x.info())
'''
类的__dict__包含的是所有自定义在类中和默认定义的方法和属性的map
实例的__dict__只是包含了通过x.a方式赋值的一个map映射，比如在__init__构造方法中
对实例属性的初始化赋值，或是创建实例后x.b赋值，都会被包含到__dict__中
'''


class M:
    def __new__(cls,**kwargs):
        '''
        该特殊方法实际上是一个静态方法，但是不需要通过通过staticmethod显示声明
        解释器会做特殊处理。
        @param: 除第一个类型参数外，其他传入的参数与传入__init__的参数保持一致
        '''
        if "error" in kwargs:
            raise RuntimeError("new cls error")
        instance = super().__new__(cls)
        instance._secret = "xuxu"
        return instance

    def __init__(self, **kwargs):
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')

m = M(a=123, b=234)
print("m._secret:", m._secret)
print("m.a:", m.a)
print("m.b", m.b)
# m = M(error=1, a=223)

#------------创建子类时的自定义方法----------------------
print("----------------init_subclass-----------------")
class H:
    def __init_subclass__(cls, default, **kwargs):
        '''创建子类时会首先调用该特殊的类方法'''
        #其实object.__init_subclass__没有做任何事
        super().__init_subclass__(**kwargs)
        cls.default = default

class K(H, default="world"):
    pass

k = K()
print("k.default:", k.default)

#对于上述用于自定义类的特殊方法中涉及的kwargs,有特殊关键字参数，都可以单独提出来，
#在创建类时传入，该特殊关键字会自动传入用于自定义类的特殊方法中



#------------类装饰器---------------------
'''
When a new class is created by type.__new__, the object provided as the namespace parameter is copied to a new ordered mapping and the original object is discarded. The new copy is wrapped in a read-only proxy, which becomes the __dict__ attribute of the class object.
'''
print("-----------------class decorator------------------")
def class_decorator(cls):
    if getattr(cls, "CONST", None) is None:
        #一旦类被创建后，其__dict__就被定义为只读的，所以类装饰器无法通过访问
        #__dict__来修改类属性了，只能通过普通的属性赋值方式
        # cls.__dict__['CONST'] = 999
        cls.CONST = 999
    return cls  

@class_decorator
class T:
    pass

# T.CONST = 110
print("T.CONST:", T.CONST)
T.CONST += 1
t = T()
t2 = T()
print("T.CONST:", T.CONST)

print("type of t:", type(t))
print("t.CONST:", t.CONST)
print("t2.CONST:", t2.CONST)
print("T.CONST:", T.CONST)
