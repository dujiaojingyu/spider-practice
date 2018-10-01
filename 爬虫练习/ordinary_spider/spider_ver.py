# import urllib.request
# import urllib.parse
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))
################################

#在python3中要这样导入模块中的方法，不然会出错
# import urllib.request
# import urllib.parse

# data = bytes(urllib.parse.urlencode({'hello':"world"}),encoding='utf-8')
# response = urllib.request.urlopen('http://httpbin.org/post',data=data)
# print(response.read())

############################################

# import urllib.request
# response = urllib.request.urlopen('http://httpbin.org/get',timeout=1)

# print(response.read())

################################
# import socket
# import urllib.request
# import urllib.error

# try:
#     response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason,socket.timeout):
#         print(e)
#         print(e.reason)
#         print('TIME OUT')
#错误有两个URLError和HTTPErro，用reason可调出错误原因
###########################################
# import urllib.request

# response = urllib.request.urlopen('http://httpbin.org')
# print(type(response))
# print(response.status)
# print(response.getheaders())#获取所有请求头
# print(response.getheader('Server'))#获取Server内容

###############################################################

# from urllib import request,parse
# url='http://httpbin.org/post'
# dic = {
#     'name':'hsj'
# }
# headers = {
#     'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
#     'Host':'httpbin.org'
# }
# data = bytes(parse.urlencode(dic),encoding='utf-8')
# req = request.Request(url=url,data=data,headers=headers,method="POST")
# response = request.urlopen(req)
# print(response.read().decode('utf-8'))

###############################################

# import urllib.request
# proxy_handler = urllib.request.ProxyHandler({
#     'http':'http://127.0.0.1:9743',
#     'https':'https://127.0.0.1:9743',
#     })
# opener = urllib.request.build_opener(proxy_handler)
# response = opener.open('http://httpbin.org')
# print(response.read())

##############################################

# import http.cookiejar,urllib.request
# cookie = http.cookiejar.CookieJar() # 将cookie赋值成一个对象
# handler = urllib.request.HTTPCookieProcessor(cookie) #生成请求头
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name+"="+item.value)

###################################
#代理
# import urllib.request
# proxy_handler = urllib.request.ProxyHandler({
#     'http':''
#     'https':''
#     })
# opener = urllib.request.builder_opener(proxy_handler)
# response = opener.open('')
# print(response.read())

##########################################
#cookie
# import urllib.request,http.cookiejar

# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.builder_opener(handler)
# response = opener.open('')
########################################################
# import urllib.request,http.cookiejar

# filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True,ignore_expires=True)

##########################################################

# import urllib.request,http.cookiejar
# filename = 'cookieLWP.txt'
# cookie = http.cookiejar.LWPCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True,ignore_expires=True)


########################################

# import http.cookiejar,urllib.request
# cookie = http.cookiejar.LWPCookieJar()
# cookie.load('cookieLWP.txt',ignore_discard=True,ignore_expires=True)
# hander = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(hander)
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))

##############################################

#urlparse
# from urllib.parse import urlparse
# result = urlparse('https://www.baidu.com/?tn=sitehao123_15')
# print(type(result),result)
from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/#comment',allow_fragments=False)
print(result)