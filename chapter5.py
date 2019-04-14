# 第五章：文件与IO
# 5.1 读写文本数据
# Read the entire file as a single string
with open('pythonTest.txt', 'rt') as f:
    data = f.read()
    print(data)

# Iterate over the lines of the file
with open('pythonTest.txt', 'rt') as f:
    for line in f:
        # process line
        print(line)
# Write chunks of text data
text1 = 'Iterate over the lines of the file'
text2 = 'Write chunks of text data'
with open('pythonTest.txt', 'a+') as f:
    f.write('\n')
    f.write(text1)
    f.write('\n')
    f.write(text2)
# 5.2 打印输出至文件中
# 在 print() 函数中指定 file 关键字参数，像下面这样：
with open('pythonTest.txt', 'a+') as f:
    print('Hello World!', file=f)

# 5.3 使用其他分隔符或行终止符打印
# 可以使用在 print() 函数中使用 sep 和 end 关键字参数，以你想要的方式输出。
print('ACME', 50, 91.5, sep=',')
print('ACME', 50, 91.5, sep=',', end='!!\n')

# 5.4 读写字节数据
# 使用模式为 rb 或 wb 的 open() 函数来读取或写入二进制数据。
# Read the entire file as a single byte string
with open('test.bin', 'rb') as f:
    data = f.read()

# Write binary data to a file
with open('test.bin', 'wb') as f:
    f.write(b'Hello World')

# 5.5 文件不存在才能写入
# 可以在 open() 函数中使用 x 模式来代替 w 模式的方法来解决这个问题
with open('pythonTest.txt', 'xt') as f:
    f.write('Hello\n')

# 5.6 字符串的I/O操作
# 使用 io.StringIO() 和 io.BytesIO() 类来创建类文件对象操作字符串数据
import io
s = io.StringIO()
s.write('Hello World\n')
print('This is a test', file=s)
print(s.getvalue())
s = io.StringIO('Hello\nWorld\n')
print(s.read(4))
print(s.read())

# 5.7 读写压缩文件
# 你想读写一个gzip或bz2格式的压缩文件
# gzip 和 bz2 模块可以很容易的处理这些文件。 两个模块都为 open() 函数提供了另外的实现来解决这个问题。
# gzip compression
import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()

# bz2 compression
import bz2
with bz2.open('somefile.bz2', 'rt') as f:
    text = f.read()
# 类似的，为了写入压缩数据，可以这样做：
# gzip compression
import gzip
with gzip.open('somefile.gz', 'wt') as f:
    f.write(text)

# bz2 compression
import bz2
with bz2.open('somefile.bz2', 'wt') as f:
    f.write(text)

# 以下没什么兴趣 先略过


