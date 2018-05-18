import re
re_name = u"^[\u4e00-\u9fa5]+"
chin = re.compile(re_name)
if chin.match(u'12312我是中国人a'):
    print "good!"
else:
    print "bad!"