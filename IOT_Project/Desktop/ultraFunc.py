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
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
GPIO.setup(GPIO_ECHO_3, GPIO.IN)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
 
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
    distance1 = (TimeElapsed * 34300) / 2
 
    return distance1
 
if __name__ == '__main__':
    try:
        while True:
            for i in range(3):
                if i == 0:
                    dist1 = distance(14, 15)
                #print ("Measured Distance1 = %.1f cm" % dist)
                if i == 1:
                    dist2 = distance(14, 18)
                #print ("Measured Distance2 = %.1f cm" % dist)
                if i == 2:
                    dist3 = distance(14, 23)
                #print ("Measured Distance3 = %.1f cm" % dist)
            print (str(dist1) + "\t" + str(dist2) + "\t" + str(dist3))
            time.sleep(0.4)

 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()