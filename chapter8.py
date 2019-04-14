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

