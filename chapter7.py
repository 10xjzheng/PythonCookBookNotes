# 第七章：函数
# 7.1 可接受任意数量参数的函数
# 为了能让一个函数接受任意数量的位置参数，可以使用一个*参数
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

# Sample use
avg(1, 2) # 1.5
avg(1, 2, 3, 4) # 2.5
# 为了接受任意数量的关键字参数，使用一个以**开头的参数
import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name=name,
                attrs=attr_str,
                value=html.escape(value))
    return element

# Example
# Creates '<item size="large" quantity="6">Albatross</item>'
make_element('item', 'Albatross', size='large', quantity=6)

# Creates '<p>&lt;spam&gt;</p>'
make_element('p', '<spam>')
# 7.2 只接受关键字参数的函数
# 你希望函数的某些参数强制使用关键字参数传递
# 将强制关键字参数放到某个*参数或者单个*后面就能达到这种效果
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, block=True) # Ok
# 7.3 给函数参数增加元信息
# 使用函数参数注解是一个很好的办法，它能提示程序员应该怎样正确使用这个函数。
def add(x:int, y:int) -> int:
    return x + y

# 7.4 返回多个值的函数
def myfun():
    return 1, 2, 3
# 7.5 定义有默认参数的函数
def spam(a, b=42):
    print(a, b)

spam(1) # Ok. a=1, b=42
spam(1, 2) # Ok. a=1, b=2

# 7.6 定义匿名或内联函数
add = lambda x, y: x + y
print(add('hello', 'world'))

# 7.7 匿名函数捕获变量值
# lambda表达式中的x是一个自由变量， 在运行时绑定值，而不是定义时就绑定
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
# 7.8 减少可调用对象的参数个数
def spam(a, b, c, d):
    print(a, b, c, d)
# 现在我们使用 partial() 函数来固定某些参数值：
from functools import partial
s2 = partial(spam, d=42) # d = 42
print(s2(1, 2, 3))

# 7.9 将单方法的类转换为函数
# 你有一个除 __init__() 方法外只定义了一个方法的类。为了简化代码，你想将它转换成一个函数
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo
# 改成：
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# Example use
# yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
# for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
#    print(line.decode('utf-8'))
# 7.10 带额外状态信息的回调函数
# 这一小节主要讨论的是那些出现在很多函数库和框架中的回调函数的使用——特别是跟异步处理有关的。
# 为了演示与测试，我们先定义如下一个需要调用回调函数的函数：
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)
def print_result(result):
    print('Got:', result)
def add(x, y):
    return x + y
apply_async(add, (2, 3), callback=print_result)
# 注意到 print_result() 函数仅仅只接受一个参数 result 。不能再传入其他信息。
# 而当你想让回调函数访问其他变量或者特定环境的变量值的时候就会遇到麻烦。
# 为了让回调函数访问外部信息，一种方法是使用一个绑定方法来代替一个简单函数。
# 比如，下面这个类会保存一个内部序列号，每次接收到一个 result 的时候序列号加1：
class ResultHandler:

    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))


# 第二种方式，作为类的替代，可以使用一个闭包捕获状态值，例如：
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler
# 还有另外一个更高级的方法，可以使用协程来完成同样的事情：
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

# 7.11 内联回调函数
# 通过使用生成器和协程可以使得回调函数内联在某个函数中。
from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper
# 这两个代码片段允许你使用 yield 语句内联回调步骤。比如：
def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')

test()
# 7.12 访问闭包中定义的变量
def sample():
    n = 0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func
f = sample()
f()
f.set_n(10)
f()
print(f.get_n())
