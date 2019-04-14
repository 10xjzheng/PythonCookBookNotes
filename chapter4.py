# 第四章：迭代器与生成器
# 4.1 手动遍历迭代器
def manual_iter():
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass

items = [1, 2, 3]
it = iter(items)
print(next(it))

# 4.2 代理迭代
# 你构建了一个自定义容器对象，里面包含有列表、元组或其他可迭代对象。 你想直接在你的这个新容器对象上执行迭代操作。
# 实际上你只需要定义一个 __iter__() 方法，将迭代操作代理到容器内部的对象上去
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

root = Node(0)
child1 = Node(1)
child2 = Node(2)
root.add_child(child1)
root.add_child(child2)
# Outputs Node(1), Node(2)
for ch in root:
    print(ch)

# 4.3 使用生成器创建新的迭代模式
# 如果你想实现一种新的迭代模式，使用一个生成器函数来定义它。
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

for n in frange(0, 4, 0.5):
    print(n)

# 4.4 实现迭代器协议
# 你想构建一个能支持迭代操作的自定义对象，并希望找到一个能实现迭代协议的简单方法
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
root = Node(0)
child1 = Node(1)
child2 = Node(2)
root.add_child(child1)
root.add_child(child2)
child1.add_child(Node(3))
child1.add_child(Node(4))
child2.add_child(Node(5))

for ch in root.depth_first():
    print(ch)

# 4.5 反向迭代
# 使用内置的 reversed() 函数
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)
# 4.6 带有外部状态的生成器函数
# 如果你想让你的生成器暴露外部状态给用户，
# 别忘了你可以简单的将它实现为一个类，然后把生成器函数放到 __iter__() 方法中过去
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()
with open('pythonTest.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
# 4.7 迭代器切片
# 函数 itertools.islice() 正好适用于在迭代器和生成器上做切片操作
# 函数 itertools.islice() 正好适用于在迭代器和生成器上做切片操作
def count(n):
    while True:
        yield n
        n += 1
c = count(0)
import itertools
for x in itertools.islice(c, 10, 20):
    print(x)
# 4.8 跳过可迭代对象的开始部分
# itertools 模块中有一些函数可以完成这个任务。 首先介绍的是 itertools.dropwhile() 函数
from itertools import dropwhile
with open('pythonTest.txt') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
# 4.9 排列组合的迭代
items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)

# 4.10 序列上索引值迭代
# 内置的 enumerate() 函数可以很好的解决这个问题
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)

# 4.11 同时迭代多个序列
# 为了同时迭代多个序列，使用 zip() 函数
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y)
# 4.12 不同集合上元素的迭代
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

# 4.13 创建数据处理管道
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

# 4.14 展开嵌套的序列
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)

# 语句 yield from 在你想在生成器中调用其他生成器作为子例程的时候非常有用。
# 如果你不使用它的话，那么就必须写额外的 for 循环了。比如：
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
        else:
            yield x
# 4.15 顺序迭代合并后的排序迭代对象
# heapq.merge() 函数可以帮你解决这个问题
import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):
    print(c)
# 4.16 迭代器代替while无限循环
# 一个常见的IO操作程序可能会想下面这样
CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        # process_data(data)

# 这种代码通常可以使用 iter() 来代替，如下所示：
def reader2(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        pass
        # process_data(data)
























