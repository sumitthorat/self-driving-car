import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData(object):
    
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8010))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # connect to a seral port
        self.ser = serial.Serial("/dev/cu.usbmodem1411", 9600, timeout=1)
        self.send_inst = True

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0
        direction = 0

        # if not os.path.exists("/training_images_raw"):
        #     os.makedirs("/training_images_raw")
        #     os.makedirs("/training_images_raw/fwd")
        #     os.makedirs("/training_images_raw/right")
        #     os.makedirs("/training_images_raw/left")
        #     os.makedirs("/training_images_raw/fwd_right")
        #     os.makedirs("/training_images_raw/fwd_left")

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
                    
                    # select lower half of the image
                    roi = image[120:240, :]
                    
                    # save streamed images
                    #cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                    
                    cv2.imshow('image', image)
                    #cv2.imshow('image', image)
                    
                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    
                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_w] and key_input[pygame.K_d]:
                                print("Forward Right")
                                #cv2.imwrite('training_images_raw/fwd_right/frame{:>05}.jpg'.format(frame), roi)
                                cv2.imwrite('training_images_raw_simple_2/fwd_right/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg',
                                            roi)
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                #self.ser.write(chr(6))
                                direction = 6

                            elif key_input[pygame.K_w] and key_input[pygame.K_a]:
                                print("Forward Left")
                                #cv2.imwrite('training_images_raw/fwd_left/frame{:>05}.jpg'.format(frame), roi)
                                cv2.imwrite('training_images_raw_simple_2/fwd_left/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg',
                                            roi)
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                direction = 7
                                #self.ser.write(chr(7))

                            elif key_input[pygame.K_s] and key_input[pygame.K_d]:
                                print("Reverse Right")
                                direction = 8
                                #self.ser.write(chr(8))
                            
                            elif key_input[pygame.K_s] and key_input[pygame.K_a]:
                                print("Reverse Left")
                                direction = 9
                                #self.ser.write(chr(9))

                            # simple orders
                            elif key_input[pygame.K_w]:
                                print("Forward")
                                #cv2.imwrite('training_images_raw/fwd/frame{:>05}.jpg'.format(frame), roi)
                                cv2.imwrite('training_images_raw_simple_2/fwd/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg',
                                            roi)
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                #self.ser.write(chr(1))
                                direction = 1

                            elif key_input[pygame.K_s]:
                                print("Reverse")
                                #saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                #self.ser.write(chr(2))
                                direction = 2
                            
                            elif key_input[pygame.K_d]:
                                print("Right")
                                #cv2.imwrite('training_images_raw/right/frame{:>05}.jpg'.format(frame), roi)
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                #saved_frame += 1
                                #self.ser.write(chr(3))
                                direction = 3

                            elif key_input[pygame.K_a]:
                                print("Left")
                                #cv2.imwrite('training_images_raw/left/frame{:>05}.jpg'.format(frame), roi)
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                #self.ser.write(chr(4))
                                direction = 4

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print 'exit'
                                self.send_inst = False
                                #self.ser.write(chr(0))
                                direction = 0
                                break
                                    
                        elif event.type == pygame.KEYUP:
                            #self.ser.write(chr(0))
                            direction = 0

                        self.ser.write(chr(direction))

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data_simple"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:    
                np.savez(directory + '/' + file_name + '_simple' + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame

        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    CollectTrainingData()