import io
import socket
import struct
import time
import picamera


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('sumitsmacbookpro.local', 8000))              # Enter ip of the server
connection = client_socket.makefile('wb')       # Return a file object associated with the socket in wb mode

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)      # sets the resolution for picamera
        camera.framerate = 10               # sets the rate to 10 frames/sec
        time.sleep(2)                       # camera initialization
        start = time.time()                 # To keep the track of time to ensure we reset after fix interval of time
        stream = io.BytesIO()               # instead of writing the contents to a file, it's written to an in memory buffer. In other words a chunk of RAM.
        # The key difference here is optimization and performance. io.BytesIO is able to do some optimizations that makes it faster than simply concatenating all the b"Hello World" one by one.
        #Concat: 1.3529 seconds
        #BytesIO: 0.0090 seconds

        
        # send jpeg format video stream
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):    #Capture continuous captures infinitely. use_video_port is used to capture faster in less time.
                                                                                        #if use_video_port is set to false it uses image_port which is slow and gives better image quality
            
            connection.write(struct.pack('<L', stream.tell()))              # It creates packets of data of size 'L' ie long to be sent Write the length of the capture to the stream and flush to  ensure it actually gets sent
            
            connection.flush()
            stream.seek(0)                                                  
            connection.write(stream.read())
            if time.time() - start > 600:        # If we've been capturing for more than 600 seconds, quit
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))      # Write 0 if we are done with the process
finally:
    connection.close()
    client_socket.close()
