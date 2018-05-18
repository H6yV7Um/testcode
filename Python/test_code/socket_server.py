# -*- coding:utf8 -*-
import socket
import time
def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen(100)
    while 1:
        try :
            connection,address = sock.accept()
            #connection.settimeout(5)
            buf = connection.recv(1024)
            print str(address)+":"+"connected"
            connection.send('you have connected to the server')
            
        except :
            sock.timeout()
            print 'timeout'
        
        connection.close()
    sock.close()

if __name__ == '__main__':
    server('localhost', 8001)