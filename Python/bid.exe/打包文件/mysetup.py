#-*- coding:utf-8 -*-
from distutils.core import setup
import py2exe

#setup(console=["helloworld.py"])
setup(windows=["bid.py"],options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}})