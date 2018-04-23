import pygame
import serial
import time

#ser = serial.Serial('com1', 9600)
ser = serial.Serial("/dev/cu.usbmodem1411", 9600)
time.sleep(2)
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("Driver")

clock = pygame.time.Clock()

white = (255,255,255)
blue = (0,0,255)
exit = False
direction =0

while not exit:
    gameDisplay.fill(white)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYDOWN:
        	key_input = pygame.key.get_pressed()

	        if key_input[pygame.K_w] and key_input[pygame.K_d]:
	        	print("Forward Right")
	        	direction = 6
	        else:
	            direction = 0

        elif event.type == pygame.KEYUP:
            direction = 0

        ser.write(chr(direction))
        pygame.display.update()

pygame.quit()
quit()