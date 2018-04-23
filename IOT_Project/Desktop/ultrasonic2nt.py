# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set GPIO Pins
GPIO_TRIGGER = 14
GPIO_ECHO_1 = 15
GPIO_ECHO_2 = 18
GPIO_ECHO_3 = 23

# set GPIO direction (IN / OUT)
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

    StartTime = time.time()
    # StartTime_2 = time.time()
    # StartTime_3 = time.time()

    StopTime_1 = 0
    StopTime_2 = 0
    StopTime_3 = 0

    count = 0

    # save StartTime
    while GPIO.input(GPIO_ECHO_1) == 0: #and GPIO.input(GPIO_ECHO_2) == 0 and GPIO.input(GPIO_ECHO_3) == 0:
        count += 1
        if(count > 10000):
            StopTime_1 = StartTime
            break;
        # save time of arrival
    # while GPIO.input(GPIO_ECHO_1) == 1 or GPIO.input(GPIO_ECHO_2)==1 or GPIO.input(GPIO_ECHO_3)==1:

    if GPIO.input(GPIO_ECHO_1) == 1:
        StopTime_1 = time.time()



    TimeElapsed_1 = StopTime_1 - StartTime
    dist = ((TimeElapsed_1 * 34300) / 2)
    print(str(dist) + "\n")


if __name__ == '__main__':
    try:
        while True:
            distance()
            # print ("Measured Distance = %.1f cm" % dist)
            #print(str(dist[0]) + "\t" + str(dist[1]) + "\t" + str(dist[2]))
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()