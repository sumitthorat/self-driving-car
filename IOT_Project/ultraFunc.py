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
        distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance(14, 15)
            print ("Measured Distance1 = %.1f cm" % dist)
            dist = distance(14, 18)
            print ("Measured Distance2 = %.1f cm" % dist)
            dist = distance(14, 23)
            print ("Measured Distance3 = %.1f cm" % dist)
            time.sleep(0.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()