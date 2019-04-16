# 第八章：类与对象
# 8.1 改变对象的字符串显示
# 要改变一个实例的字符串表示，可重新定义它的 __str__() 和 __repr__() 方法。例如：
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)
# __repr__() 方法返回一个实例的代码表示形式，通常用来重新构造这个实例。
# 内置的 repr() 函数返回这个字符串，跟我们使用交互式解释器显示的值是一样的。
# __str__() 方法将实例转换为一个字符串，使用 str() 或 print() 函数会输出这个字符串。比如：
p = Pair(3, 4)
print(p)

# 8.2 自定义字符串的格式化
# 为了自定义字符串的格式化，我们需要在类上面定义 __format__() 方法。例如：
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
d = Date(2012, 12, 21)
print(format(d))
print(format(d, 'mdy'))
s = 'The date is {:ymd}'.format(d)
print(s)

# 8.3 让对象支持上下文管理协议
# 为了让一个对象兼容 with 语句，你需要实现 __enter__() 和 __exit__() 方法
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None
from functools import partial

conn = LazyConnection(('www.python.org', 80))
# Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
# 8.4 创建大量对象时节省内存方法
# 对于主要是用来当成简单的数据结构的类而言，你可以通过给类添加
#_slots__ 属性来极大的减少实例所占的内存。比如：
class Date:
    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
# 8.5 在类中封装属性名
# Python程序员不去依赖语言特性去封装数据，而是通过遵循一定的属性和方法命名规约来达到这个效果。
#  第一个约定是任何以单下划线_开头的名字都应该是内部实现。比如：
class A:
    def __init__(self):
        self._internal = 0 # An internal attribute
        self.public = 1 # A public attribute

    def public_method(self):
        '''
        A public method
        '''
        pass

    def _internal_method(self):
        pass
# 8.6 创建可管理的属性
# 自定义某个属性的一种简单方法是将它定义为一个property。
# 例如，下面的代码定义了一个property，增加对一个属性简单的类型检查：
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
a = Person('Guido')
print(a.first_name)
a.first_name = 'qqq'

# 8.7 调用父类方法
# 为了调用父类(超类)的一个方法，可以使用 super() 函数，比如
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # Call parent spam()
# 8.8 子类中扩展property
# 如果你仅仅只想扩展property的某一个方法，那么可以像下面这样写：
class SubPerson(Person):
    @Person.first_name.getter
    def first_name(self):
        print('Getting name')
        return super().name
# 或者，你只想修改setter方法，就这么写：
class SubPerson(Person):
    @Person.first_name.setter
    def first_name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).first_name.__set__(self, value)


# 8.9 创建新的类或实例属性
# 如果你想创建一个全新的实例属性，可以通过一个描述器类的形式来定义它的功能。下面是一个例子：
# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# 一个描述器就是一个实现了三个核心的属性访问操作(get, set, delete)的类， 分别为 __get__()
# __set__() 和 __delete__() 这三个特殊的方法。 这些方法接受一个实例作为输入，之后相应的操作实例底层的字典。
# 为了使用一个描述器，需将这个描述器的实例作为类属性放到一个类的定义中。例如：
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
# 当你这样做后，所有对描述器属性(比如x或y)的访问会被 __get__() 、__set__() 和 __delete__() 方法捕获到。例如：
p = Point(2, 3)
print(p.x)
# p.x = 2.3 # TypeError: Expected an int

# 8.10 使用延迟计算属性
# 你想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。
# 但是一旦被访问后，你希望结果值被缓存起来，不用每次都去计算。
# 定义一个延迟属性的一种高效方法是通过使用一个描述器类，如下所示：
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
# 你需要像下面这样在一个类中使用它：
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius
# 下面在一个交互环境中演示它的使用：
c = Circle(4.0)
print(c.radius)
print(c.area)
print(c.area)
print(c.perimeter)
print(c.perimeter)

# 仔细观察你会发现消息 Computing area 和 Computing perimeter 仅仅出现一次
# 这种方案有一个小缺陷就是计算出的值被创建后是可以被修改的。例如：
c.area = 25
print(c.area)

# 8.11 简化数据结构的初始化
# 你写了很多仅仅用作数据结构的类，不想写太多烦人的 __init__() 函数
# 可以在一个基类中写一个公用的 __init__() 函数：
import math

class Structure1:
    # Class variable that specifies expected fields
    _fields = []

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

# Example class definitions
class Stock(Structure1):
    _fields = ['name', 'shares', 'price']

class Point(Structure1):
    _fields = ['x', 'y']

class Circle(Structure1):
    _fields = ['radius']

    def area(self):
        return math.pi * self.radius ** 2
# 8.12 定义接口或者抽象基类
# 使用 abc 模块可以很轻松的定义抽象基类：
from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass
class SocketStream(IStream):
    def read(self, maxbytes=-1):
        print('read')
        pass

    def write(self, data):
        pass

socket = SocketStream()
socket.read()

# 8.13 实现数据模型的类型约束
# 8.14 实现自定义容器
# 8.15 属性的代理访问
# 8.16 在类中定义多个构造器
# 8.17 创建不调用init方法的实例
# 8.18 利用Mixins扩展类功能
# 8.19 实现状态对象或者状态机
# 8.20 通过字符串调用对象方法
# 8.21 实现访问者模式
# 8.22 不用递归实现访问者模式
# 8.23 循环引用数据结构的内存管理
# 8.24 让类支持比较操作
# 8.25 创建缓存实例
