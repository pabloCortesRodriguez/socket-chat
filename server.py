import socket
import threading
import pickle
import sys

class Server:
    def __init__(self, host='localhost', port=4000):
        self.clients = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        accept = threading.Thread(target=self.accept_conn)
        process = threading.Thread(target=self.process_conn)

        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()

        while True:
            msg = str(input('->'))
            if msg == 'exit':
                self.sock.close()
                sys.exit()
            else:
                pass

    def msg_to_all(self, msg, client):
        for c in self.clients:
            try:
                if c != client:
                    c.send(msg)
            except:
                self.clients.remove(c)

    def accept_conn(self):
        print('accepting connection')
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clients.append(conn)
            except:
                pass

    def process_conn(self):
        print('processing connection')
        while True:
            if len(self.clients) > 0:
                for client in self.clients:
                    try:
                        data = client.recv(1024)
                        if data:
                            self.msg_to_all(data,client)
                    except:
                        pass

s = Server()
