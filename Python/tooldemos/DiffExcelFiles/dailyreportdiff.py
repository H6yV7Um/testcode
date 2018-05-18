#coding:utf-8

"""
脚本用途：读取两个excel文件做对比，输出一个diff文件
"""


import xlrd
import sys
import os
from fuzzywuzzy import fuzz
reload(sys)
sys.setdefaultencoding('utf-8')

def readExcel(source):
    ws = xlrd.open_workbook(source)
    a = ws.sheet_by_index(0)
    return  a

def readIntoList(sheet):
  a = []
  for i in range(1,sheet.nrows):
    a.append(' '.join([str(value) for value in sheet.row_values(i)]))
  return a

COUNT = 0     

palo = readExcel('palo_acticonfig.xlsx')    #读取palo导出execel的数据
#gpdb = readExcel('DailyReport/20161205acticonf.xlsx')
gpdb = readExcel('gpdb_acticonfig.xlsx')

palorows = readIntoList(palo)
gpdbrows = readIntoList(gpdb)

print "running..."
print "delete last result file..."
if os.path.exists('diff.txt'):
  os.remove('diff.txt')
for prow in palorows:
  if prow in gpdbrows:
    COUNT+=1
    gpdbrows.remove(prow)     #相同的则从gpdb删除，最后剩下不同的
  else:
    with open('diff.txt','a') as f:
      f.write(str(prow) + '\n')
if len(gpdbrows) != 0:
  with open('diff.txt','a') as f:
    f.writelines("----------------------------gegegege--------------------------\n")
    for value in [str(row) for row in gpdbrows]:
      f.writelines(value+"\n")
    
print "palo count: %s" % repr(palo.nrows-1)
print "gpdb count: %s" % repr(gpdb.nrows-1)
print "same count : %s" % COUNT
print "done!"








