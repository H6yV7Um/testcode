import struct
import socketserver

class EchoServer(socketserver.BaseRequestHandler):
    '''用于本地调试收发消息'''
    # def handle_bak(self):
    #     text = 'helloworld'.encode()
    #     fmt = '>HIQ%ss' % len(text)
    #     text_data = struct.pack(fmt, 88, 24, 1024999, text)
    #     print(text)
    #     self.request.send(text_data)
    #     self.request.send(text_data)
    #     data = self.request.recv(1024)
    #     print("source data length:",len(data))
    #     fmt = '>10s'
    #     print("source data:", data)
    #     print("unpack data:", struct.unpack(fmt, data))
    #     self.request.send(data)
    #     # data = struct.pack('>Q', 6666)
    #     # self.request.send(data)

    def handle(self):
        print("Client connected:", self.client_address)
        data = self.request.recv(1024)
        print("received source data:", data)
        self.request.send(data)

s1=socketserver.ThreadingTCPServer(("127.0.0.1",6000), EchoServer)
s1.serve_forever()