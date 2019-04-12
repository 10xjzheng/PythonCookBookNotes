# 第三章：数字日期和时间
# 3.1 数字的四舍五入
print(round(1.23, 1))
print(round(1.25361,3))

# 3.2 执行精确的浮点数运算
a = 4.2
b = 2.1
print(a + b) # 出问题

# 精确一点
from decimal import Decimal
a = Decimal('4.2')
b = Decimal('2.1')
print(a + b)

# 3.3 数字的格式化输出
x = 1234.56789
print(format(x, '0.2f'))
# Right justified in 10 chars, one-digit accuracy
print(format(x, '>10.1f'))
# Left justified
print(format(x, '<10.1f'))

# 3.4 二八十六进制整数
x = 1234
print(bin(x)) # 二进制
print(oct(x)) # 八进制
print(hex(x)) # 十六
# 也可以用format
print(format(x, 'b'))
print(format(x, 'o'))
print(format(x, 'x'))

# 3.5 字节到大整数的打包与解包
# 你有一个字节字符串并想将它解压成一个整数。或者，你需要将一个大整数转换为一个字节字符串。
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(len(data))
print(int.from_bytes(data, 'little'))
int.from_bytes(data, 'big')
x = 94522842520747284487117727783387188
print(x.to_bytes(16, 'big'))
print(x.to_bytes(16, 'little'))

# 3.6 复数的数学运算
a = complex(2, 4)
b = 3 - 5j
print(a + b)

# 3.7 无穷大与NaN
import math
a = float('inf')
b = float('-inf')
c = float('nan')
print(math.isinf(a))
print(math.isnan(c))

# 3.8 分数运算
from fractions import Fraction
a = Fraction(5, 4)
b = Fraction(7, 16)
print(a + b)

# 3.9 大型数组运算
# 涉及到数组的重量级运算操作，可以使用 NumPy 库
import numpy as np
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])
print(ax * 2)
print(ax + 10)
print(ax * ay)

# 3.10 矩阵与线性代数运算
m = np.matrix([[1, -2, 3], [0, 4, 5], [7, 8, -9]])
print(m)
# Return transpose
print(m.T)
# Return inverse
print(m.I)

# 3.11 随机选择
import random
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))
print(random.sample(values, 2))
# 打乱序列中元素的顺序
print(random.shuffle(values))
# 生成随机整数
print(random.randint(0,10))

# 3.12 基本的日期与时间转换
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
print(c.days)
print(c.seconds)
from datetime import datetime
a = datetime(2012, 9, 23)
print(a + timedelta(days=10))
now = datetime.today()
print(now)

# 3.13 计算最后一个周五的日期
from datetime import datetime, timedelta
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']
def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date
print(datetime.today())
print(get_previous_byday('Monday'))
print(get_previous_byday('Friday'))
# 上面的算法原理是这样的：先将开始日期和目标日期映射到星期数组的位置上(星期一索引为0)，
# 然后通过模运算计算出目标日期要经过多少天才能到达开始日期。然后用开始日期减去那个时间差即得到结果日期。
# 3.14 计算当前月份的日期范围
from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)
a_day = timedelta(days=1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

# 3.15 字符串转换为日期
from datetime import datetime
text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
print(z - y)

from datetime import datetime
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
print(d)
central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)
