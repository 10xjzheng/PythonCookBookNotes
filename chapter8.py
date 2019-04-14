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

