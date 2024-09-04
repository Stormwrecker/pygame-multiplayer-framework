import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 20
        self.addr = (self.server, self.port)
        self.data_size = 2048
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(self.data_size))
        except socket.error as e:
            pass

    def trade(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(self.data_size))
        except socket.error as e:
            print(e)

