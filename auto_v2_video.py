from keras.models import load_model
import serial
import numpy as np
import threading
import socket
import cv2
import time
from multiprocessing.connection import Listener

sensor_data = None

#stop_sign_cascade = cv2.CascadeClassifier("AutoRCCar-master/computer/cascade_xml/stop_sign.xml")

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

class UltraStreamHandler(object):

    def __init__(self):
        self.serv = Listener(('', 9002))
        self.client = self.serv.accept()
        self.handle()

    def handle(self):
        global sensor_data
        while True:
            while True:
                sensor_data = self.client.recv()
                if not sensor_data.count('.') > 1:
                    sensor_data = round(float(sensor_data), 1)
    # def handle(self):
    #     global sensor_data
    #     try:
    #         while True:
    #             self.data = self.request.recv(1024)
    #             sensor_data = round(float(self.data), 1)
    #             print(sensor_data)
    #
    #     finally:
    #         print("ultrasonic connection closed!")

class VideoStreamHandler(object):

    model = load_model("65_simple_acc_2.h5")

    rc_control = SendToCar()

    ultra_thread = threading.Thread(target=UltraStreamHandler)
    ultra_thread.start()

    def __init__(self):
        self.server_socket = socket.socket()  # Creating socket default parameters:  socket.AF_INET, socket.SOCK_STREAM
        self.server_socket.bind(('0.0.0.0', 8101))  # or 0.0.0.0 for all interfaces
        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()  # Returns connection object to share data and address of client
        self.connection = self.connection.makefile('rb')  # Return a file object associated with the socket in rb mode
        self.handle()

    def handle(self):
        global sensor_data

        stream_bytes = ' '  # to accept data

        while True:

            stream_bytes += self.connection.read(1024)
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

                # stop_sign = stop_sign_cascade.detectMultiScale(gray, 1.3, 5)
                # for (x, y, w, h) in stop_sign:
                #     cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
                #     roi_gray = gray[y:y + h, x:x + w]
                #     f = 3.6
                #     x = 0.0014 * w
                #     X = 66
                #
                #     d = ((X * f) / x)
                #     d = (d + (0.4 * d)) / 100

                if sensor_data is not None and sensor_data < 20:
                    self.rc_control.send(99)
                    print("Stop")
                    #time.sleep(6)
                else:
                    self.rc_control.send(prediction)

                if cv2.waitKey(1) & 0xFF == ord(
                        'q'):  # To execute the quit condition. waitkey() waits for the user to enter a key for given period of time else it waits indefinitely
                    cv2.destroyAllWindows()
                    self.rc_control.send(99)
                    break


if __name__ == "__main__":
    VideoStreamHandler()





