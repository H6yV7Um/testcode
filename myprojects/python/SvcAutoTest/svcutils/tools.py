import json
import datetime
import decimal
import base64

class DotDict(dict):
    '''Wrapper of ordinary dict, support nested when making assignment with a dot'''
    def __init__(self, dictobj):
        for key, value in dictobj.items():
            self.__setattr__(key, value)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = self.__class__(value)
        else:
            self[key] = value

    def __missing__(self, key):
        raise KeyError("{} object has no key '{}'".format(self, key))
        # return '{' + key + '}'


class CJsonEncoder(json.JSONEncoder):  
    """JSON serialization tool class, converted to string for special data types"""
    def default(self, obj):  
        if isinstance(obj, bytes):
            return bytes.decode(obj)
        elif isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, datetime.date):  
            return obj.strftime("%Y-%m-%d")  
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 

def unit32_to_ip(n):
    '''Converting an integer IP into a standard IP address format'''
    return '%d.%d.%d.%d' % (n>>24,(n>>16)&0x00ff,(n>>8)&0x0000ff,n&0x000000ff)

def bin_to_b64str(b):
    '''Binary converted to B64 encoded string'''
    if not isinstance(b, bytes):
        raise TypeError("param must be bytes")
    return base64.b64encode(b)