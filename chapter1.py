# 1.1 解压序列赋值给多个变量
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, (year, mon, day) = data
print(name, shares, price, year, mon, day)

# 1.2 解压可迭代对象赋值给多个变量
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
first, *middle, last = record
print(middle)

# 1.3 保留最后 N 个元素
# python作用域 http://python.jobbole.com/86465/

from collections import deque


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            previous_lines.append(line)
            yield line, previous_lines


with open(r'./pythonTest.txt') as f:
    for line, prevlines in search(f, 'python', 3):
        print('prevlines'+'-' * 20)
        for pline in prevlines:
            print(pline, end='')
        print('line'+'-' * 20)
        print(line, end='')
        print('-' * 30)

# 1.4 查找最大或最小的 N 个元素
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]


# 1.5 实现一个优先级队列

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
print(q.pop())
print(q.pop())
print(q.pop())

# 1.6 字典中的键映射多个值
from collections import defaultdict
from collections import defaultdict
d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)

d = defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
for key, val in d.items():
    print('key: %s value: %s' % (key, val))

# 1.7 字典排序
# 为了能控制一个字典中元素的顺序，你可以使用 collections 模块中的 OrderedDict 类。
# 在迭代操作的时候它会保持元素被插入时的顺序

from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4
# Outputs "foo 1", "bar 2", "spam 3", "grok 4"
for key in d:
    print(key, d[key])

# 1.8 字典的运算
# 怎样在数据字典中执行一些计算操作（比如求最小值、最大值、排序等等）？
# 执行这些计算的时候，需要注意的是 zip() 函数创建的是一个只能访问一次的迭代器。
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
min_price = min(zip(prices.values(), prices.keys()))
# min_price is (10.75, 'FB')
max_price = max(zip(prices.values(), prices.keys()))
# max_price is (612.78, 'AAPL')
print(min_price, max_price)

# 1.9 查找两字典的相同点
a = {
    'x' : 1,
    'y' : 2,
    'z' : 3
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}
# Find keys in common
print(a.keys() & b.keys()) # { 'x', 'y' }
# Find keys in a that are not in b
print(a.keys() - b.keys()) # { 'z' }
# Find (key,value) pairs in common
print(a.items() & b.items()) # { ('y', 2) }

# 1.10 删除序列相同元素并保持顺序


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
print(list(dedupe(a, key=lambda d: (d['x'],d['y']))))

# 1.11 命名切片
record = '....................100 .......513.25 ..........'
SHARES = slice(20, 23)
PRICE = slice(31, 37)
cost = int(record[SHARES]) * float(record[PRICE])
print(SHARES, PRICE, cost)

# 1.12 序列中出现次数最多的元素
words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
from collections import Counter
word_counts = Counter(words)
# 出现频率最高的3个单词
top_three = word_counts.most_common(3)
print(top_three)
# Outputs [('eyes', 8), ('the', 5), ('look', 4)]

# 1.13 通过某个关键字排序一个字典列表
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]
from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print('rows_by_fname'+ '-' * 20)
print(rows_by_fname)
print('rows_by_uid'+ '-' * 20)
print(rows_by_uid)
# 1.14 排序不支持原生比较的对象
# 你想排序类型相同的对象，但是他们不支持原生的比较操作。


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


def sort_notcompare():
    users = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=lambda u: u.user_id))


sort_notcompare()
# 另外一种方式是使用 operator.attrgetter() 来代替 lambda 函数
from operator import attrgetter
users = [User(23), User(3), User(99)]
print(sorted(users, key=attrgetter('user_id')))

# 1.15 通过某个字段将记录分组
rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]
from operator import itemgetter
from itertools import groupby

# Sort by the desired field first
rows.sort(key=itemgetter('date'))
# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)

# 1.16 过滤序列元素
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
print([n for n in mylist if n > 0])
# 使用列表推导的一个潜在缺陷就是如果输入非常大的时候会产生一个非常大的结果集，占用大量内存。
#  如果你对内存比较敏感，那么你可以使用生成器表达式迭代产生过滤的元素。
pos = (n for n in mylist if n > 0)
print(pos)
for x in pos:
    print(x)

# 1.17 从字典中提取子集
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
# Make a dictionary of all prices over 200
p1 = {key: value for key, value in prices.items() if value > 200}
# Make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(p1, p2)

# 1.18 映射名称到序列元素
# 你有一段通过下标访问列表或者元组中元素的代码，但是这样有时候会使得你的代码难以阅读，
# 于是你想通过名称来访问元素。
# collections.namedtuple() 函数通过使用一个普通的元组对象来帮你解决这个问题。
# 这个函数实际上是一个返回 Python 中标准元组类型子类的一个工厂方法。
# 你需要传递一个类型名和你需要的字段给它，然后它就会返回一个类，你可以初始化这个类，
# 为你定义的字段传递值等
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
print(sub.addr, sub.joined)

# 1.19 转换并同时计算数据
# 你需要在数据序列上执行聚集函数（比如 sum() , min() , max() ）， 但是首先你需要先转换或者过滤数据
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
print(s)
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

# 1.20 合并多个字典或映射
# 现在有多个字典或者映射，你想将它们从逻辑上合并为一个单一的映射后执行某些操作，
# 比如查找值或者检查某些键是否存在。
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
from collections import ChainMap
c = ChainMap(a,b)
print(c['x']) # Outputs 1 (from a)
print(c['y']) # Outputs 2 (from b)
print(c['z']) # Outputs 3 (from a)
