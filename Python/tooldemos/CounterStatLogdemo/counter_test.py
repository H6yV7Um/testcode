#coding:utf-8
import os
import re
import shutil
from collections import Counter


def godness():
    """字符串迭代"""
    for i in 'aaaaaaaaaaaaaaaaaddddddddddddddddddddgggggggggggggggggeeeeeeeeeeeeeeeeeeeejjjjjjjjjjjjjkkkkkkkkssssssss':
        yield i 

def test_counter():
    """读取文件，过滤IP生成器函数"""
    pata = re.compile(r'OnTimer')
    patb = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')   #ip正则
    with open('server.log','rb') as f:
        for line in f:
            #yield line
            m = patb.findall(line)
            if m:
                yield m[0]
            else:
                pass
            
def start_counter():
    """新建counter实例，统计数量"""
    c = Counter(godness())
    print c.items()
    print "start counting the number of ip"
    c = Counter(test_counter())
    print "各IP地址访问量统计：%s" % c.items()
    print "访问量前三的IP地址：%s" % c.most_common(3)
    print "访问总量：%s" % sum(c.values())
    print "字典形式统计：%s" % dict(c)
    print "finished!"


def make_archive():
    """shutil打包,分块读取文件练习"""
    srcfile = os.path.join(os.path.dirname(__file__), 'npMyEditBox.log')
    dstfile = os.path.join(os.path.dirname(__file__), 'test\\test.log')
    archive_name = os.path.join(os.path.dirname(__file__), 'apple')
    root_dir = os.path.dirname(dstfile)
    shutil.copy(srcfile, dstfile)
    shutil.make_archive(archive_name, 'gztar', root_dir=root_dir)
    with open(dstfile,'rb') as f:
        for line in f:
            if line:
                print line.strip('\n\r')
          
        while True:
            chunk = f.read(1000)
            if chunk:
                print chunk
                print "next 1000bytes"
            else:
                print "the end!"
                break

def write_file():
    """循环写入文件，为测试代码提供测试数据"""
    with open('server.log','rb') as f:
        data = f.read()
    print "start writing file,please wait..."
    for i in xrange(10):
        with open('server.log','a') as f:
            f.write(data)
    print "finished!"


if __name__ == '__main__':
    #write_file()
    start_counter()


'''
"""正则匹配练习"""
pat=re.compile(r'(\d{9})+')
l=[111111111222233333,222222222,3333,444444444, 999999999 ,888888888]
s=str(l)
print type(s)
print pat.findall(s)

def test():
    for i in range(5):
        yield i
t=test()
m=t.next()
b=t.next()
d=t.next()
print m+b+d
l=['abc','sdf','Gdgd','Ere']
print sorted(l)
def namesorted(a,b):
    return cmp(a.lower(),b.lower())
print sorted(l,namesorted)


re_name = u"http://product\.suning\.com/\d+\.html"
chin = re.compile(re_name)
if chin.match(u'http://product.suning.com/45645.html'):
    print "good!"
else:
    print "bad!"

'''      



