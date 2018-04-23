import socket
import time
import cv2


class SensorStreamingTest(object):
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8004))
        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()
        self.streaming()

    def streaming(self):

        try:
            print "Connection from: ", self.client_address
            start = time.time()

            while True:
                sensor_data = float(self.connection.recv(1024))
                print "Distance: %0.1f cm" % sensor_data
                if cv2.waitKey() == ord('q'):
                    break



        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    SensorStreamingTest()