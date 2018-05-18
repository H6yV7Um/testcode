
'''
python中关于类的传奇故事可谓不胜枚举，今天就聊一聊关于类的前世今生，话说五百年前...咳咳~言归正传
其实就是类是如何创建的以及怎样自定义一个类的创建过程。关于这个话题笔者总结五个部分，下面且一一道来。
一、metaclass
要自定义一个类的创建过程首先想到的就是通过元类来实现，直接通过一个例子来逐一解释类是如何
创建的。
'''
#例子1-1
class BaseMeta(type):
    def __new__(cls, name, bases, nsdict, **kwds):
        clsobj = type.__new__(cls, name, bases, nsdict)
        return clsobj

    def __prepare__(name, bases, **kwds):
        return type.__prepare__(name, bases)

class A(metaclass=BaseMeta):
    def test_a(self):
        print("test_a")

class B(A):
    def test_b(self):
        print("test_b")
'''
通过元类是如何创建一个类呢，总体分为四步：
1、首先确定要使用的元类，请参考第三部分
2、执行元类的__prepare__方法，该方法必须返回一个类字典对象，只要实现了类似字典添加值和
查询遍历方法的对象即可。所返回的类字典对象用来存放所创建的类的namespace。
该方法是可选的，如果不重写该方法，默认会调用type.__prepare__，返回一个普通的dict
如上边例子所示。
3、然后解释器会根据类的定义（比如例子中的类A的定义）计算class body，搜集类的相关信息放到对应
参数中：类的名称"A"传入name；父类列表传入bases(bases实际是一个元组)；namespace相关的
传入nsdict，namespace又包括两部分：一部分是类中所定义的方法或者类变量，比如test_a方法，
另一部分是元类预定义或是在计算class body过程中搜集的应该放到这个类的namespace中的信息，
这一部分不需要特别关注。
4、最后会调用元类的__new__方法来创建并返回这个类对象，name会成为类的__name__属性，
bases成为类的__bases__属性，nsdict会被复制一份，该复制品被包装为只读的，并赋值为
为类的__dict__属性。如果不重写该方法，则默认会调用type.__new__，如例子中所示。
至此，一个热气腾腾的新鲜类就诞生了。(当然解释器还会执行些其他细微的操作，不在讨论范围内，直接忽略)
说明：
1、name，bases，nsdict这三个参数名字可以随便定义，没有固定要求，但最好定义为便于理解
的形式。
2、__new__的第一个位置参数cls指代的是定义__new__方法的类，例子中就代表BaseMeta类。
其实该方法如果定义在一个普通类中，则返回的是该类的实例对象了，从而可以自定义实例的创建过程。
后边会给出一个例子，感兴趣可以瞅一眼,然后经过仔细琢磨你会发现其实元类就相当于类的一个特殊父类。
与平时所说的实例的父类有异曲同工之妙。
3、如果方法声明了可选的关键字参数**kwds，则定义类的时候可以传入关键字参数，会通过例子说明具体如何
使用。

了解了类的创建过程，就可以改变某个步骤来实现自定义的需求了，下边通过几个例子简单演示一下：
'''

'''
1、标准例子，拿来主义（官档抄的=o=）
'''
#例子1-2
class PrepareMeta(type):
    def __prepare__(name, bases):
        import collections
        nsdict = collections.OrderedDict()
        nsdict['default_ns'] = "I'm default"
        return nsdict

    def __new__(cls, name, bases, namespace):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.members = tuple(namespace)
        return result

class P(metaclass=PrepareMeta):
    def test_one(self):
        pass
    def test_two(self):
        pass

print("P.members:", P.members)
'''
例子中将P的namespace定义为一个OrderedDict，并添加了default_ns，从输出中可以看出
default_ns是第一个，也就是__prepare__先执行的，然后开始计算class body，然后依次添加
到namespace中，一部分是解释器添加的必要属性，另一部分就是类定义体中的。
tips：pyhton3.3及以上版本输出中才会有__qualname__
'''

'''
2、接收关键字参数的类定义
'''
#例子1-3
class KeywordsMeta(type):
    def __prepare__(name, bases, order=False, **kwds):
        if order:
            import collections
            print("Return OrderedDict")
            return collections.OrderedDict()
        return {}

    def __new__(cls, name, bases, nsdict, **kwds):
        cls_obj = type.__new__(cls, name, bases, nsdict)
        if "members" in kwds:
            cls_obj.members = kwds['members']
        else:
            cls_obj.members = None
        return cls_obj

class K(metaclass=KeywordsMeta, order=True, members=[1,2,3]):
    pass

print("K.members:", K.members)
'''
在定义类的时候，metaclass之后的关键字参数都会被添加到kwds中，有特殊用途的关键字参数
可以提取出来，比如例子中的order。
'''

'''
3、小试牛刀
'''
#例子1-4
class DisinitMeta(type):
    def __call__(cls, *args, **kwds):
        raise RuntimeError("臣妾做不到啊")

class D(metaclass=DisinitMeta):
    pass

# D()
'''
该例子演示了通过元类的方式如何禁止类实例化，当然实现该功能的方法有很多，这里不作过多说明
'''
#例子1-5
class InitMeta(type):
    def __init__(cls, name, bases, nsdict):
        if '__module__' in nsdict:
            cls.init = "HelloWorld"
        
class I(metaclass=InitMeta):
    pass

print('I.init:', I.init)
'''
在元类中定义一个__init__特殊方法来给类做些初始化的操作，其实该方法与__new__很像，唯一不同
的就是参数cls，__new__中代表的是元类，而__init__中代表的是被创建的类，也就是执行顺序问题。
'''

'''
二、通过type动态创建类
我们知道type用处最多的是用来获取对象的类型即type(object)。同时type也是所有元类的基类，
定义类的时候没有声明元类的话默认则为type，当给它传入三个参数时type(name, bases, nsdict)
即可用来创建一个类，参数的意义同上所述。
'''
#例子2-1
class Y:
    CONST = 999
    def __init__(self):
        self.m = 1
        self.n = 2
    def info(self):
        print("I'm ", type(self).__name__)
X = type('X', (Y,),{'a':1, 'func':lambda self,x,y: x+y})
'''
类X等价于以下定义
class X(Y):
    a = 1
    def func(self, x, y):
        return x+y
'''
'''
通过type创建类的语法就可以看出，其实类就是元类的实例，
从这个角度其实就很好理解某些特殊方法了，比如__new__声明在普通类中是用来创建实例的，而放在
元类中则是用来创建类的；__call__声明在普通类中用来控制实例调用，而声明在元类中用来控制
类调用;__init__声明在普通类是用来初始化实例，而声明在元类中则可以用来初始化类，就像在
在例子1-4中所示的那样，只是在传参上有所区别。
通过代码也可以很直观的验证这一点：
'''
print("isinstance(X, type):", isinstance(X, type))

'''
通过输出可以看到X是type的实例，当然type是默认的元类
即使不通过type创建类X，上边的判断也是成立的，我们基于例子1-1来看下：
'''
print("isinstance(A, BaseMeta):", isinstance(A, BaseMeta))
print("isinstance(B, BaseMeta):", isinstance(B, BaseMeta))
'''
通过输出可以很明显的看出类就是元类的实例，而且元类可以通过继承的方式传递，所以B也是BaseMeta
的实例。
'''
'''
三、通过标准库types.new_class也可以创建类，这里不过过多说明了，直接通过源码可以看到
原理都是一样的
'''
def new_class(name, bases=(), kwds=None, exec_body=None):
    """Create a class object dynamically using the appropriate metaclass."""
    meta, ns, kwds = prepare_class(name, bases, kwds)
    if exec_body is not None:
        exec_body(ns)
    return meta(name, bases, ns, **kwds)

def prepare_class(name, bases=(), kwds=None):
    if kwds is None:
        kwds = {}
    else:
        kwds = dict(kwds) # Don't alter the provided mapping
    if 'metaclass' in kwds:
        meta = kwds.pop('metaclass')
    else:
        if bases:
            meta = type(bases[0])
        else:
            meta = type
    if isinstance(meta, type):
        # when meta is a type, we first determine the most-derived metaclass
        # instead of invoking the initial candidate directly
        meta = _calculate_meta(meta, bases)
    if hasattr(meta, '__prepare__'):
        ns = meta.__prepare__(name, bases, **kwds)
    else:
        ns = {}
    return meta, ns, kwds

def _calculate_meta(meta, bases):
    """Calculate the most derived metaclass."""
    winner = meta
    for base in bases:
        base_meta = type(base)
        if issubclass(winner, base_meta):
            continue
        if issubclass(base_meta, winner):
            winner = base_meta
            continue
        # else:
        raise TypeError("metaclass conflict: "
                        "the metaclass of a derived class "
                        "must be a (non-strict) subclass "
                        "of the metaclasses of all its bases")
    return winner
'''
有一点需要补充的：创建类的第一步是要确定使用的元类，用语言描述可能比较抽象，故意放到这里借助
_calculate_meta这段代码来说明，代码逻辑很清晰，总结来说就是要么使用type，要么使用元类继承
关系中最上层的子元类。
'''

'''
其实不论通过哪种方式创建类，原理都是一样的，只是表现形式不同。接下来要介绍的两部分
跟类的创建过程没有关系，而是在类创建后再进行改造，即所谓的post-processing。
'''

'''
四、类装饰器
装饰器地球人都知道，类装饰器只是其中的一个应用分支，也比较简单易懂，看例子
'''
def class_decorator(cls):
    if getattr(cls, "CONST", None) is None:
        # cls.__dict__['CONST'] = 999 #not work
        cls.CONST = 999
    return cls  

@class_decorator
class T:
    pass

print("T.CONST:", T.CONST)
'''
很简单的一个例子，有点需要强调下，一旦类被创建并初始化后，其namespace也就是类的__dict__
属性就成为只读的了，无法修改赋值。
'''
'''
五、__init_subclass__
这个特殊方法是3.6新增的，当父类定义了这个方法，其子类在创建后会紧接着执行该方法，同样支持
可选关键字参数。
'''
class Person:
    def __init_subclass__(cls, name, **kwds):
        #object.__init_subclass__没有做任何操作，但是传入参数会报错
        super().__init_subclass__()
        cls.name = name

class XiaoMing(Person, name="ligoudan"):
    pass

print("XiaoMing's name:", XiaoMing.name)
'''
关于以上这几点，这里更多的是想阐述清楚其基本原理，至于具体用途还是取决于真实的场景。
就笔者遇到的实际情况而言，metaclass和类装饰器用到的比较多，尤其是类装饰器，因为遇到的
大部分场景都是post-processing的，类装饰器可以很优雅的完成这一任务。
https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
https://www.python.org/dev/peps/pep-3115/
'''