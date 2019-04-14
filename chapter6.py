# 第六章：数据编码和处理
# 6.1 读写CSV数据
import csv
with open('test.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print(row)
# 6.2 读写JSON数据
# 使用 json.dump() 和 json.load() 来编码和解码JSON数据
import json
data = {
    'name': 'ACME',
    'shares': 100,
    'price': 542.23
}
json_str = json.dumps(data)
print(json_str)
print(type(json_str))
data = json.loads(json_str)
print(data)
print(type(data))

# 6.3 解析简单的XML数据
from urllib.request import urlopen
from xml.etree.ElementTree import parse

# Download the RSS feed and parse it
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# Extract and output tags of interest
for item in doc.iterfind('channel/item'):
    link = item.findtext('link')
    print(link)
    print()
# 6.4 增量式解析大型XML文件
# 任何时候只要你遇到增量式的数据处理时，第一时间就应该想到迭代器和生成器
from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass
# 6.5 将字典转换为XML
from xml.etree.ElementTree import Element

def dict_to_xml(tag, d):
    '''
    Turn a simple dict of key/value pairs into XML
    '''
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
e = dict_to_xml('stock', s)
from xml.etree.ElementTree import tostring
print(tostring(e))
# 6.6 解析和修改XML
# 你想读取一个XML文档，对它最一些修改，然后将结果写回XML文档
from xml.etree.ElementTree import parse, Element
doc = parse('test.xml')
root = doc.getroot()
print(root)
root.remove(root.find('sri'))
root.remove(root.find('cr'))
root.getchildren().index(root.find('nm'))
e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)
#doc.write('test.xml', xml_declaration=True)

# 6.7 利用命名空间解析XML文档
# 你想解析某个XML文档，文档中使用了XML命名空间。
class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)
    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'
    def __call__(self, path):
        return path.format_map(self.namespaces)
ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
print(doc.find(ns('content/{html}html')))
print(doc.findtext(ns('content/{html}html/{html}head/{html}title')))
# 6.8 与关系型数据库的交互
# 略过 这个要重点学习的，这里只是略微介绍而已
# 6.9 编码和解码十六进制数
s = b'hello'
import binascii
h = binascii.b2a_hex(s)
print(h)
print(binascii.a2b_hex(h))
# 6.10 编码解码Base64数据
s = b'hello'
import base64
a = base64.b64encode(s)
print(a)
print(base64.b64decode(a))