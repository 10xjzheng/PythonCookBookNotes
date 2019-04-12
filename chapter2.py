# 2.1 使用多个界定符分割字符串
import re
line = 'asdf fjdk; afed, fjek,asdf, foo'
print(re.split(r'[;,\s]\s*', line))
print(re.split(r'(;|,|\s)\s*', line))

# 2.2 字符串开头或结尾匹配
filename = 'spam.txt'
print(filename.endswith('.txt'))
print(filename.startswith('file:'))

# 2.3 用Shell通配符匹配字符串
# 你想使用 Unix Shell 中常用的通配符(比如 *.py , Dat[0-9]*.csv 等)去匹配文本字符串
# fnmatch 模块提供了两个函数—— fnmatch() 和 fnmatchcase() ，可以用来实现这样的匹配
from fnmatch import fnmatch, fnmatchcase
print(fnmatch('foo.txt', '*.txt'))
print(fnmatch('foo.txt', '?oo.txt'))
# 如果你对这个区别很在意，可以使用 fnmatchcase() 来代替
fnmatch('foo.txt', '*.TXT') # On OS X (Mac) false
fnmatch('foo.txt', '*.TXT') # On Windows true

# 2.4 字符串匹配和搜索
import re

text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
print(re.match(r'\d+/\d+/\d+', text1))

datepat = re.compile(r'\d+/\d+/\d+')
print(datepat.match(text1), datepat.match(text2))

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
m = datepat.match(text1)
print(m.group(0), m.group(1), m.group(2), m.group(3))
print(m.groups())

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
print(datepat.findall(text))
for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))

# 2.5 字符串搜索和替换
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah', 'yep')
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))
# 如果你打算用相同的模式做多次替换，考虑先编译它来提升性能
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2', text)
# 对于更加复杂的替换，可以传递一个替换回调函数来代替，比如：
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
# 2.6 字符串忽略大小写的搜索替换
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags=re.IGNORECASE)
re.sub('python', 'snake', text, flags=re.IGNORECASE)

# 2.7 最短匹配模式
# 你正在试着用正则表达式匹配某个文本模式，但是它找到的是模式的最长可能匹配。 而你想修改它变成查找最短的可能匹配。
str_pat = re.compile(r'"(.*)"')
text1 = 'Computer says "no."'
print(str_pat.findall(text1))
# 在这个例子中，模式 r'\"(.*)\"' 的意图是匹配被双引号包含的文本。 但是在正则表达式中*操作符是贪婪的，因此匹配操作会查找最长的可能匹配。
text2 = 'Computer says "no." Phone says "yes."'
print(str_pat.findall(text2))
# 为了修正这个问题，可以在模式中的*操作符后面加上?修饰符
str_pat = re.compile(r'"(.*?)"')
print(str_pat.findall(text2))

# 2.8 多行匹配模式
# 你正在试着使用正则表达式去匹配一大块的文本，而你需要跨越多行去匹配。
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
 multiline comment */
'''
print(comment.findall(text1))
# 查不到
print(comment.findall(text2))

#为了修正这个问题，你可以修改模式字符串，增加对换行的支持
# ?: 用于关闭捕获
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
print(comment.findall(text2))

# 2.9 将Unicode文本标准化
# 你正在处理Unicode字符串，需要确保所有字符串在底层有相同的表示
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1 == s2)
# normalize() 第一个参数指定字符串标准化的方式。
# NFC表示字符应该是整体组成(比如可能的话就使用单一编码)，而NFD表示字符应该分解为多个组合字符表示
import unicodedata
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
print(t1 == t2)

print(ascii(t1))
t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
print(t3 == t4)

# 2.10 在正则式中使用Unicode
# 混合使用Unicode和正则表达式通常会让你抓狂。 如果你真的打算这样做的话，最好考虑下安装第三方正则式库，
# 它们会为Unicode的大小写转换和其他大量有趣特性提供全面的支持，包括模糊匹配。
pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'
pat.match(s) # Matches
pat.match(s.upper()) # Doesn't match
print(s.upper())

# 2.11 删除字符串中不需要的字符
# strip() 方法能用于删除开始或结尾的字符。 lstrip() 和 rstrip() 分别从左和从右执行删除操作。
s = ' hello world \n'
print(s.strip())

# 2.12 审查清理文本字符串
s = 'pýtĥöñ\fis\tawesome\r\n'
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None # Deleted
}
a = s.translate(remap)
print(a)
# 正如你看的那样，空白字符 \t 和 \f 已经被重新映射到一个空格。回车字符r直接被删除。
# 代码越简单运行越快。 对于简单的替换操作， str.replace() 方法通常是最快的，甚至在你需要多次调用的时候
# 你就会发现这种方式会比使用 translate() 或者正则表达式要快很多。

# 2.13 字符串对齐
text = 'Hello World'
print(text.ljust(20))
print(text.rjust(20))
print(text.center(20))

# 2.14 合并拼接字符串
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
print(' '.join(parts))
print(','.join(parts))
a = 'Is Chicago'
b = 'Not Chicago?'
print(a + ' ' + b)
c = 'aaa'
# 字符串合并可能看上去并不需要用一整节来讨论。 但是不应该小看这个问题，程序员通常在字符串格式化的时候因为选择不当而给应用程序带来严重性能损失。
# 最重要的需要引起注意的是，当我们使用加号(+)操作符去连接大量的字符串的时候是非常低效率的， 因为加号连接会引起内存复制以及垃圾回收操作。
print(a + ':' + b + ':' + c) # Ugly
print(':'.join([a, b, c])) # Still ugly
print(a, b, c, sep=':') # Better

# 2.15 字符串中插入变量
s = '{name} has {n} messages.'
print(s.format(name='Guido', n=37))

name = 'Guido'
n = 37
print(s.format_map(vars()))

# 2.16 以指定列宽格式化字符串
# 你有一些长字符串，想以指定的列宽将它们重新格式化
import textwrap
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."
print(textwrap.fill(s, 70))
print(textwrap.fill(s, 40))
# 2.17 在字符串中处理html和xml
# 你想将HTML或者XML实体如 &entity; 或 &#code; 替换为对应的文本。 再者，你需要转换文本中特定的字符(比如<, >, 或 &)。
s = 'Elements are written as "<tag>text</tag>".'
import html
print(s)
print(html.escape(s))
print(html.escape(s, quote=False)) # 引号

s = 'Spicy &quot;Jalape&#241;o&quot.'