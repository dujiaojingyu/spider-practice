
import re

def multiple_replace(text, idict): 
    rx = re.compile('|'.join(map(re.escape, idict))) 
    print('rx:',rx) 
    def one_xlat(match):  
        print('one_xlat:',match)
        return idict[match.group(0)] 
    return rx.sub(one_xlat, text) #sub启用的是match匹配


replace_dict = {
    '<div id="content">':'',
    ' ':'xxx',
    '<p>':'',
    '</p>':'',
    '<div>':'',
    '</div>':''
}

xxx = multiple_replace('a<p>fsdf jh</p>as<div> oj i</div>f',replace_dict)
print('xxx:',xxx)