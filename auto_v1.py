from keras.models import load_model
from keras.models import Sequential
import keras
import serial
import numpy as np
import socket
import threading
import cv2
import time

use_opencv = False
stop_sign_cascade = cv2.CascadeClassifier("AutoRCCar-master/computer/cascade_xml/stop_sign.xml")








class VideoStreaming(object):
    def __init__(self):

        # self.server_socket_2 = socket.socket()
        # self.server_socket_2.bind(("0.0.0.0", 8004))
        # self.server_socket_2.listen(1)
        # self.connection_2, self.client_address_2 = self.server_socket_2.accept()

        self.server_socket = socket.socket()  # Creating socket default parameters:  socket.AF_INET, socket.SOCK_STREAM
        self.server_socket.bind(('0.0.0.0', 8101))  # or 0.0.0.0 for all interfaces
        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()  # Returns connection object to share data and address of client
        self.connection = self.connection.makefile('rb')  # Return a file object associated with the socket in rb mode
        self.streaming()





    def streaming(self):
        if use_opencv == False:
            model = load_model("65_simple_acc_2.h5")
        else:
            model = cv2.ml.ANN_MLP_load('IOT_Project/mlp_xml/mlp_1522120028.xml')
        ser = serial.Serial("/dev/cu.usbmodem1411", 9600)
        time.sleep(2)

        try:
            print "Connection from: ", self.client_address
            print "Press 'q' to exit"

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

                    stop_sign = stop_sign_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in stop_sign:
                        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        roi_gray = gray[y:y + h, x:x + w]
                        f = 3.6
                        x = 0.0014 * w
                        X = 66

                        d = ((X * f) / x) / 100

                        print("d" + str(d))

                    if use_opencv == False:
                        roi = roi.reshape((38400))

                        roi = np.array(roi, dtype="float") / 255.0

                        roi = np.expand_dims(roi, axis=0)

                        prediction = model.predict_classes(roi)



                        if prediction == 0:
                            print("Fwd")
                            ser.write(chr(1))
                            time.sleep(0.06)
                        elif prediction == 1:
                            print("Left")
                            ser.write(chr(7))
                            time.sleep(0.06)
                        else:
                            print("Right")
                            ser.write(chr(6))
                            time.sleep(0.06)

                    else:
                        roi = roi.reshape((1, 38400)).astype(np.float32)
                        ret, resp = model.predict(roi)
                        prediction = resp.argmax(-1)

                        if prediction == 2:
                            print("Fwd")
                            ser.write(chr(1))
                        elif prediction == 0:
                            print("Left")
                            ser.write(chr(7))
                        else:
                            print("Right")
                            ser.write(chr(6))

                    #time.sleep(0.5)













                    if cv2.waitKey(1) & 0xFF == ord(
                            'q'):  # To execute the quit condition. waitkey() waits for the user to enter a key for given period of time else it waits indefinitely
                        break  # ord() returns the ascii value of the specified character

        finally:
            self.connection.close()
            self.server_socket.close()
            ser.write(chr(0))


if __name__ == '__main__':
    VideoStreaming()