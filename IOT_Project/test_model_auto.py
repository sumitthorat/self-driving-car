#pythfrom keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os
import socket



class VideoStreamingTest(object):
    def __init__(self):

        self.server_socket = socket.socket()            #Creating socket default parameters:  socket.AF_INET, socket.SOCK_STREAM
        self.server_socket.bind(('0.0.0.0', 8002))  # or 0.0.0.0 for all interfaces
        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()      # Returns connection object to share data and address of client
        self.connection = self.connection.makefile('rb')    #Return a file object associated with the socket in rb mode
        self.streaming()
        self.model = load_model("test_model.model")

    def pre_process(self, raw_image):
        image_arr = np.array(raw_image)
        image_arr = test_image.astype('float32')
        image_arr /= 255
        image_arr = np.expand_dims(image_arr, axis=3) 
        image_arr = np.expand_dims(image_arr, axis=0)
        return image_arr

    def streaming(self):

        try:
            #print("Connection from: ", self.client_address
            stream_bytes = ' '          # to accept data     
            
            while True:
                
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')       #\xff\xd8 and \xff\xd9 represents the headers of the image and we are extracting that using find()
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:              # Returns -1 if not found
                    
                    jpg = stream_bytes[first:last + 2]      #Extracting first image
                    stream_bytes = stream_bytes[last + 2:]  #Moving the pointer to next image by slicing
                    
                    #image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    raw_image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)   #Decoding the image using numpy for efficiency
                    cv2.imshow('image', raw_image)
                    roi = raw_image[120:240, :]
                    image_arr = self.pre_process(roi)
                    prediction = model.predict_classes(image_arr)
                    print(prediction)



                    if cv2.waitKey(1) & 0xFF == ord('q'):   # To execute the quit condition. waitkey() waits for the user to enter a key for given period of time else it waits indefinitely
                        break                               # ord() returns the ascii value of the specified character
        
        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    VideoStreamingTest()
