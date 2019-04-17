# 第十一章：网络与Web编程

# 11.1 作为客户端与HTTP服务交互
from urllib import request, parse

# Base URL being accessed
url = 'http://httpbin.org/get'

# Dictionary of query parameters (if any)
parms = {
   'name1': 'value1',
   'name2': 'value2'
}

# Encode the query string
querystring = parse.urlencode(parms)

# Make a GET request and read the response
u = request.urlopen(url+'?' + querystring)
resp = u.read()
print(resp)

# 11.2 创建TCP服务器
from socketserver import BaseRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:

            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()

# 11.3 创建UDP服务器
from socketserver import BaseRequestHandler, UDPServer
import time

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), self.client_address)

if __name__ == '__main__':
    serv = UDPServer(('', 20000), TimeHandler)
    serv.serve_forever()

# 11.4 通过CIDR地址生成对应的IP地址集
# 你有一个CIDR网络地址比如“123.45.67.89/27”，你想将其转换成它所代表的所有IP （比如，“123.45.67.64”, “123.45.67.65”, …, “123.45.67.95”))
import ipaddress
net = ipaddress.ip_network('123.45.67.64/27')
for a in net:
    print(a)
