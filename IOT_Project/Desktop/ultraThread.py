import time
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig1 = 14
echo1 = 15
trig2 = 23
echo2 = 24
trig3 = 25
echo3 = 8


GPIO.setup(trig1, GPIO.OUT)
GPIO.setup(trig2, GPIO.OUT)
GPIO.setup(trig3, GPIO.OUT)
GPIO.setup(echo1, GPIO.IN)
GPIO.setup(echo2, GPIO.IN)
GPIO.setup(echo3, GPIO.IN)

def distance(trig, echo):
	# set Trigger to HIGH
    GPIO.output(trig, True)
 	# set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

def get_distance(trig, echo, tab):
	while True:
		dist = distance(trig, echo)
		if tab == 0:
			print (str(tab)+" = "+str(dist))
		if tab == 1:
			print (str(tab)+" = " + str(dist))
		if tab == 2:
			print (str(tab)+" = "+ str(dist))
		
		time.sleep(0.5)

	

t1 = threading.Thread(target=get_distance, args=(14,15,0))
t2 = threading.Thread(target=get_distance, args=(23,24,1))
t3 = threading.Thread(target=get_distance, args=(25,8,2))

if __name__ == "__main__":
	t1.start()
	t2.start()
	t3.start()




