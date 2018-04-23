from keras.models import load_model
from keras.models import Sequential
import keras
import serial
import numpy as np
import SocketServer
import threading
import cv2
import time

sensor_data = None

class SendToCar(object):

    def __init__(self):
        self.ser = serial.Serial("/dev/cu.usbmodem1411", 9600)

    def send(self, prediction):
        if prediction == 0:
            print("Fwd")
            self.ser.write(chr(1))
            time.sleep(0.08)
        elif prediction == 1:
            print("Left")
            self.ser.write(chr(7))
            time.sleep(0.08)
        elif prediction == 2:
            print("Right")
            self.ser.write(chr(6))
            time.sleep(0.08)
        else:
            self.ser.write(chr(0))
            time.sleep(0.08)

class UltraStreamHandler(SocketServer.BaseRequestHandler):
    data = " "

    def handle(self):
        global sensor_data
        try:
            while True:
                self.data = self.request.recv(1024)
                sensor_data = round(float(self.data), 1)
                print(sensor_data)

        finally:
            print("ultrasonic connection closed!")

class VideoStreamHandler(SocketServer.StreamRequestHandler):

    model = load_model("65_simple_acc_2.h5")

    rc_control = SendToCar()

    def handle(self):
        global sensor_data

        stream_bytes = ' '  # to accept data

        while True:

            stream_bytes += self.rfile.read(1024)
            first = stream_bytes.find(
                '\xff\xd8')  # \xff\xd8 and \xff\xd9 represents the headers of the image and we are extracting that using find()
            last = stream_bytes.find('\xff\xd9')
            if first != -1 and last != -1:  # Returns -1 if not found

                jpg = stream_bytes[first:last + 2]  # Extracting first image
                stream_bytes = stream_bytes[last + 2:]  # Moving the pointer to next image by slicing

                # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                    0)  # Decoding the image using numpy for efficiency
                cv2.imshow('image', gray)

                roi = gray[120:320, :]

                roi = roi.reshape((38400))

                roi = np.array(roi, dtype="float") / 255.0

                roi = np.expand_dims(roi, axis=0)

                prediction = self.model.predict_classes(roi)

                if sensor_data is not None and sensor_data < 20:
                    self.rc_control.send(99)
                    print("Stop")
                else:
                    self.rc_control.send(prediction)

                if cv2.waitKey(1) & 0xFF == ord(
                        'q'):  # To execute the quit condition. waitkey() waits for the user to enter a key for given period of time else it waits indefinitely
                    cv2.destroyAllWindows()
                    self.rc_control.send(99)
                    break








class ThreadServers(object):

    video_port = 8025
    ultra_port = 8026

    def video_server_thread(self):
        video_server = SocketServer.TCPServer(('0.0.0.0', 8025), VideoStreamHandler)
        video_server.serve_forever()

    def ultra_server_thread(self):
        ultra_server = SocketServer.TCPServer(('0.0.0.0', 8026), UltraStreamHandler)
        ultra_server.serve_forever()

    video_thread = threading.Thread(target=video_server_thread, args=(1,))
    print("video server started on " + str(video_port))
    video_thread.start()

    ultra_thread = threading.Thread(target=ultra_server_thread, args=(1,))
    print("ultra server started on " + str(ultra_port))
    ultra_thread.start()






if __name__ == "__main__":
    ThreadServers()





