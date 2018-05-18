#-*- coding:utf-8 -*-
import urllib2
import pytesseract
#import PIL
from PIL import Image
#import ImageShow
#import _imaging
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

fp=urllib2.urlopen('https://www.imfreevpn.org/scode.php')
print fp

name="D:\\image\\1.jpg"
f=open(name,'wb')
f.write(fp.read())
time.sleep(2)
f.close()

fl=open(name,'rb')
image=Image.open(fl)
#image.show()
image.load()
vcode=pytesseract.image_to_string(image)
if vcode:
	print vcode 
else:
	print "identify failed"
fl.close()



