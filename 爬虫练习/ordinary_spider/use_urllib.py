#urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,*, cafile=None, capath=None, cadefault=False, context=None)
#get类型请求
# from urllib import request

# response = request.urlopen('http://www.baidu.com') # response对象
# #response.read()读取对象,读取到的数据为bytes类型，必须decode
# print(response.read().decode('utf-8'))

#####################################

#post类型请求
from urllib import request
from urllib import parse#解析

data = bytes(parse.urlencode({'world':'hello'}),encoding='utf-8')
response = request.urlopen('http://httpbin.org/post',data=data)
print(response.read())