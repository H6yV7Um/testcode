#!/opt/venv_python2.7.13/bin/
#coding:utf-8

from fabric.api import *


def main():
    '''Function Doc'''
    local("fab -f batch_update.py start")



if __name__ == '__main__':
    main()
