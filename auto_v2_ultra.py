import socket
from multiprocessing.connection import Client



class UltraStreamHandler(object):


    def __init__(self):
        self.server_socket = socket.socket()
        self.data = " "
        self.c = Client(('localhost', 9002))
        self.server_socket.bind(('0.0.0.0', 8100))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.handle()

    def handle(self):

        try:
            while True:
                self.data = self.connection.recv(1024)
                #sensor_data = round(float(self.data), 1)
                self.c.send(self.data)
                print(self.data)

        finally:
            print("ultrasonic connection closed!")

if __name__ == '__main__':
    UltraStreamHandler()
