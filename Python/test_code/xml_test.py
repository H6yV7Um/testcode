#coding: utf-8

try:
    import xml.etree.cElementTree as ET
except ImportError, e:
    import xml.etree.ElementTree as ET
import sys

''' xml module pratice'''

#<?xml...?>必须为xml字符串的第一行，否则读取报错
root = '''<?xml version="1.0"?>      
<data> 
  <country name="Singapore"> 
    <rank>4</rank> 
    <year>2011</year> 
    <gdppc>59900</gdppc> 
    <neighbor name="Malaysia" direction="N"/> 
  </country> 
  <country name="Panama"> 
    <rank>68</rank> 
    <year>2011</year> 
    <gdppc>13600</gdppc> 
    <neighbor name="Costa Rica" direction="W"/> 
    <neighbor name="Colombia" direction="E"/> 
  </country> 
</data> 
'''
if ET.iselement(root):
  pass
else:
  root = ET.fromstring(root)
##root = ET.fromstring(xml)
#root = ET.XML(xml)         #该方法同fromstring一样，都返回element对象
print ET.iselement(root)
print root[0][1].tag,"------",root[0][1].text
for child in root:
    print child.tag,"-----",child.attrib
    print child.find("rank").text
    for subchild in child:
        print subchild.tag,subchild.text        #节点标签名字，节点内容



