# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import re
# import time
# import requests
# #目标网页
# url = 'https://www.biquge5200.cc/75_75584/'
# #模拟浏览器发送http请求
# response = requests.get(url)
# #编码方式
# response.encoding = 'gbk'
# #获取目标网页的源码
# html = response.text
# html.encode('utf-8')
# #获取小说名字
# title = re.findall(r'<meta property="og:title" content="(.*?)"/>',html)[0]
# #打开一个文件
# f = open('%s.txt'%title,'w',encoding='utf-8')
# #获取章节内容部分源码
# dd = re.findall(r'<dt>\《剑来\》正文</dt>.*?</dl>',html,re.S)[0]
# #获取章节名称
# chapter_info_list = re.findall(r'<dd><a href="(.*?)">(.*?)</a></dd>',dd)
# for chapter_info in chapter_info_list:
#     chapter_url,chapter_title = chapter_info
#     #下载章节内容
#     chapter_response = requests.get(chapter_url)
#     chapter_response.encoding = 'gbk'
#     #获取整页源代码
#     chapter_html = chapter_response.text
#     #获取章节内容
#     chapter_content = re.findall(r'<div id="content"><p>.*?</div>',chapter_html,re.S)[0]
#     #清理数据
#     chapter_content = chapter_content.replace('<div id="content">','')
#     chapter_content = chapter_content.replace(' ','')
#     chapter_content = chapter_content.replace('<p>','')
#     chapter_content = chapter_content.replace('</p>','')
#     chapter_content = chapter_content.replace('<div>','')
#     chapter_content = chapter_content.replace('</div>','')

#     f.write(chapter_title)
#     f.write(chapter_content)
#     f.write('\n')
#     time.sleep(0.3)
# f.close()

########################################################

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import time
import requests

url = 'https://www.biquge5200.cc/75_75584/'

#多个目标替换
def multiple_replace(text, idict):  
    rx = re.compile('|'.join(map(re.escape, idict)))  
    def one_xlat(match):  
        return idict[match.group(0)]  
    return rx.sub(one_xlat, text) 

#抽取html整页源码
def get_html(url):
    response = requests.get(url)
    response.encoding = 'gbk'
    html = response.text
    return html

#提取小说名以及章节和对应的url
html = get_html(url)
title = re.findall(r'<meta property="og:title" content="(.*?)"/>',html)[0]
f = open('%s.txt'%title,'w',encoding='utf-8')
chapter_info_list = re.findall(r'<dd.*?href="(.*?)">(.*?)</a>',html,re.S)

#替换字典
replace_dict = {
    '<div id="content">':'',
    ' ':'',
    '<p>':'',
    '</p>':'',
    '<div>':'',
    '</div>':''
}
#具体小说内容
for chapter_info in chapter_info_list:
    chapter_url,chapter_title = chapter_info
    chapter_html = get_html(chapter_url)
    chapter_content = re.findall(r'<div id="content"><p>.*?</div>',chapter_html,re.S)[0]
    chapter_content= multiple_replace(chapter_content,replace_dict)
    f.write(chapter_title)
    f.write(chapter_content)
    f.write('\n')
    time.sleep(0.3)   #运行太快服务器限制，加上睡眠时间便可解决
f.close()