#coding:utf-8


import os
import subprocess
import sys
import re
from collections import deque

useage = """
useage: statistic the num of parsed result
eg: python statistic.py meituan 20160810
"""
if len(sys.argv) == 3:
    file_list = os.listdir(".")
    #print sys.argv[1], sys.argv[2]
    pat = re.compile('^%s.+\.%s$' % (sys.argv[1],sys.argv[2]))
    target_list = deque([])
    for f in file_list:
        if pat.match(f):
            target_list.appendleft(f)
    #print "\n".join(target_list)
    if target_list:
        total = 0
        print "-"*55
        for n in target_list:
            cmd = subprocess.Popen('cat %s|wc -l' % n, shell=True, stdout=subprocess.PIPE)
            num = cmd.stdout.read()
            num = int(num.strip("\n"))
            print "{0:<40}|{1:<15,}".format(n, num)
            print "-"*55
            total+=num                                                          
        print "total:%s" % total
    else:
        print "file not found, check the params"
else:
    print useage