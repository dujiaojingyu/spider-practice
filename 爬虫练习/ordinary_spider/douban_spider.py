import re
import requests
url = "https://book.douban.com/"

content = requests.get(url).text
print(content)
# res_obj = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?publisher">(.*?)</span>.*?</li>',re.S)
# res_obj = re.compile('<a href="(.*?)".*?</a>',re.S)
res_obj = re.compile('<li.*?cover.*?<a href="(.*?)".*?</a>',re.S)
url = re.findall(res_obj,content)
name = re.findall('<li.*?cover.*?title="(.*?)".*?</a>',content,re.S)
author = re.findall('<li.*?author">(.*?)</div>',content,re.S)
year = re.findall('<li.*?year">(.*?)</span>',content,re.S)
results = zip(url,name,author,year)
f = open('douban.txt','w',encoding='utf-8')
for result in results:
    url,name,author,date= result
    naem = re.sub(r'\s','',name)
    author = re.sub(r'\s','',author)
    date = re.sub(r'\s','',date)
    #,name,author,date,publisher
    print(url,name,author,date)
    f.write(url)
    f.write(name)
    f.write(author)
    f.write(date)
    f.write('\n')
    # f.write(publisher)
f.close()