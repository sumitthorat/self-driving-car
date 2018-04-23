#Libraries
import RPi.GPIO as GPIO
import time
 
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

distance_list = []
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime_1 = time.time()
    StartTime_2 = time.time()
    StartTime_3 = time.time()
    
    StopTime_1 = time.time()
    StopTime_2 = time.time()
    StopTime_3 = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_1) == 0 or GPIO.input(GPIO_ECHO_2)==0 or GPIO.input(GPIO_ECHO_3)==0:
        
        if GPIO.input(GPIO_ECHO_1)==0:
            StartTime_1 = time.time()

        if GPIO.input(GPIO_ECHO_2)==0:
            StartTime_2 = time.time()

        if GPIO.input(GPIO_ECHO_3)==0:
            StartTime_3 = time.time()            
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_1) == 1 or GPIO.input(GPIO_ECHO_2)==1 or GPIO.input(GPIO_ECHO_3)==1:
        
        if GPIO.input(GPIO_ECHO_1)==1:
            StopTime_1 = time.time()

        if GPIO.input(GPIO_ECHO_2)==1:
            StopTime_2 = time.time()

        if GPIO.input(GPIO_ECHO_3)==1:
            StopTime_3 = time.time()
 
    # time difference between start and arrival
    TimeElapsed_1 = StopTime_1 - StartTime_1
    TimeElapsed_2 = StopTime_2 - StartTime_2
    TimeElapsed_3 = StopTime_3 - StartTime_3
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance_list.append((TimeElapsed_1 * 34300) / 2)
    distance_list.append((TimeElapsed_2 * 34300) / 2)
    distance_list.append((TimeElapsed_3 * 34300) / 2)

 
    return distance_list
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            print(str(dist[0]) + "\t" + str(dist[1]) + "\t" + str(dist[2]))
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()