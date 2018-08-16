import socket
import threading
import pickle
import sys

class Client:
    def __init__(self, host='localhost', port=4000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        msg_recv = threading.Thread(target=self.msg_recv)
        msg_recv.daemon = True
        msg_recv.start()

        while True:
            msg = str(input(''))
            if msg == 'exit':
                self.sock.close()
                sys.exit()
            else:
                self.send_msg(msg)

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print('-', pickle.loads(data))
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))

c = Client()
