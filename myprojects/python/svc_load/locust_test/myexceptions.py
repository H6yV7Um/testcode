#coding:utf-8

class OperateTimeout(Exception):
    '''svc service response timeout error'''
    pass

class ResponseError(Exception):
    '''svc response code non zero error'''
    pass

class ConnectionError(Exception):
    '''socket connection error'''
    pass

class UnexpectError(Exception):
    '''UnexpectError'''
    pass