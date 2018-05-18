from socketserver import BaseRequestHandler
from socketserver import ThreadingTCPServer


class EchoServer(BaseRequestHandler):
    def handle(self):
        print("Client connected:", self.client_address)
        data = self.request.recv(4096)
        print("Received pb data:", data)
        self.request.send(data)

server = ThreadingTCPServer(("127.0.0.1", 6000), EchoServer)
server.serve_forever()