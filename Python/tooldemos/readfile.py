#coding:utf-8


import re
import os
import Queue
import threading
import multiprocessing
from multiprocessing import freeze_support
import time
import argparse
from functools import wraps
#from tomorrow import threads

class HandleFile(object):
    """docstring for HandleFile"""
    def __init__(self, fname, nfname='test.log'):
        super(HandleFile, self).__init__()
        self.fname = fname
        self.nfname = nfname
        self._fobj = open(fname, 'r+')
        self._nfobj = open(nfname, 'w+')

    def _fgenerator(self):    
        #文件对象只能被读取一次，重复读取返回空,所以要reopen
        self._reopen()
        for line in self._fobj:
            yield line
        self._fobj.close()

    def _full_text(self, size=-1):
        self._reopen()
        content = self._fobj.read(size)
        self._fobj.close()
        return content

    def _compile(self, pattern, flag=0):
        return re.compile(pattern, flag)

    def replace_full_text(self, source, repl):
        self._reopen(1)
        pat = self._compile(source, re.M)
        #re.subn返回一个元组(替换后的内容,替换次数)
        sub_tuple = pat.subn(repl, self._full_text())
        self._write(sub_tuple[0])
        print "%s matches are replaced" % sub_tuple[1]
        #每次替换后关闭新文件，防止其他替换重复写文件
        self.close()

    def replace_each_line(self, source, repl):
        self._reopen(1)
        pat = self._compile(source)
        num = 0
        for line in self._fgenerator():
            self._write(pat.subn(repl, line)[0])
            num += pat.subn(repl, line)[1]
        print "%s matches are replaced" % num
        self.close()

    def _write(self, text, lsep='\n'):
        self._nfobj.write(text.rstrip() + lsep)

    def close(self):
        if not self._nfobj.closed:
            self._nfobj.close()

    def _reopen(self, flag=None):
        if flag is None and self._fobj.closed:
            self._fobj = open(self.fname, 'r+')
        elif flag and self._nfobj.closed:
            self._nfobj = open(self.nfname, 'w+')

class Timer:
    def __init__(self, func=time.time):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


source_queue = multiprocessing.Queue()
result_queue = multiprocessing.Queue()

def threads(n, async=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            for i in range(n):
                tname = "%s Thread-%s start" % (func.__name__, i)
                t = threading.Thread(target=func, args=args, name=tname)
                #t = multiprocessing.Process(target=func, args=args, name=tname)
                t.daemon = True
                t.start()
                print "%s start!" % t.name
            if not async:
                t.join()
        return wrapper
    return decorator

def tthreads(n):
    pool = multiprocessing.Pool(n)
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            pool.apply_async(func, args)
        return wrapper
    return decorator

@threads(5)
def reader(f):
    try:
        while True:
            source_queue.put(next(f))
            f.flush()
    except Exception, e:
        if not f.closed:
            f.close()
        print "done"


def readfile(fname):
    f = open(fname)
    reader(f)
    '''
    for line in f:
        if line:
            source_queue.put(line)
    '''
@threads(10, async=False)
def writer(f):
    while True:
        try:
            newline, num = result_queue.get(timeout=1)
            f.write(newline)
            #total_num += num
        except Queue.Empty:
            break

def writefile(newfile):
    total_num = 0
    with open(newfile, 'w+') as f:
        writer(f)
    print "Task done!"
    print "%s matches are replaced!" % total_num



def replace_line(line, pat, repl):
    repat = re.compile(pat)
    return repat.subn(repl, line)

@threads(10)
def worker(pat, repl):
    while True:
        try:
            source_line = source_queue.get(timeout=1)
            new_item = replace_line(source_line, pat, repl)
            result_queue.put(new_item)
        except Queue.Empty:
            break

def start(source_file,newfile, pat, repl):
    with Timer() as t:
        readfile(source_file)
        worker(pat, repl)
        writefile(newfile)
    print "elapsed time: %.2fs" % t.elapsed




if __name__ == '__main__':
    '''
    fhandler = HandleFile('test.txt')
    #fhandler.replace_full_text(r'\d+', 'helloworld')
    fhandler.replace_each_line(r'\d+', 'helloworld')
    fhandler.close()
    '''
    freeze_support()
    parser = argparse.ArgumentParser(description="process files")
    parser.add_argument('-s', metavar="source-file", dest="source_file", \
                                    action="store", required=True)
    parser.add_argument('-n', metavar="new-file", dest="new_file", \
                                    action="store", default="test.log")
    parser.add_argument('-p', metavar="re-pattern", dest="repat", action="store", required=True)
    parser.add_argument('-r', metavar="replaced-string", dest="repl", action="store", required=True)
    args = parser.parse_args()
    start(args.source_file, args.new_file, args.repat, args.repl)
