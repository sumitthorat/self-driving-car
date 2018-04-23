import time
import RPi.GPIO as GPIO
import os,sys

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 14
GPIO_ECHO_1 = 15
GPIO_ECHO_2 = 18
GPIO_ECHO_3 = 23

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
GPIO.setup(GPIO_ECHO_3, GPIO.IN)

# restart_time = time.time()
#prog_start_time = time.time() 



def restart():
    print("Restarted")
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
 
def distance(GPIO_ECHO):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    time_limit = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
       
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
    	StopTime = time.time()
    	if time.time() - time_limit > 0.01:
            return -1
    
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    time.sleep(0.01)
 
    return distance

def get_distance():
	readings_ctr = 0
	prog_start_time = time.time()
	while True:
	    dist1 = distance(GPIO_ECHO_1)
	    #time.sleep(0.02)
	    dist2 = distance(GPIO_ECHO_2)
	    #time.sleep(0.02)
	    dist3 = distance(GPIO_ECHO_3)
	    time.sleep(0.4)
	    readings_ctr += 1
		#print(str(dist1) + "\t" + str(dist2) + "\t" + str(dist3))
	    print("%.2f \t %.2f \t %.2f " % (dist1, dist2, dist3))
	    #print(str(dist1) + "\t" + str(i))

	    if readings_ctr == 10:
	    	print("Time for execution = %.3f" % (time.time() - prog_start_time))
	    	restart()
       # if(time.time() - restart_time > 10):
    	#     restart()

if __name__ == "__main__":
	get_distance()
    
