import pygame
import serial
import time

ser = serial.Serial('/dev/cu.usbmodem1441', 9600)
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
            if event.key == pygame.K_w:
                print("Up")
                direction = 1
            if event.key == pygame.K_s:
                print("Down")
                direction = 2
            if event.key == pygame.K_a:
                print("Left")
                direction = 7
            if event.key == pygame.K_d:
                print("Right")
                direction = 6
            '''if event.key == pygame.K_LEFT and event.key == event.pygame.K_UP:
                print("Up Left")
                direction = 5
            if event.key == pygame.K_RIGHT and event.key == event.pygame.K_UP:
                print("Up Left")
                direction = 6
            if event.key == pygame.K_LEFT and event.key == event.pygame.K_DOWN:
                print("Up Left")
                direction = 7
            if event.key == pygame.K_RIGHT and event.key == event.pygame.K_DOWN:
                print("Up Left")
                direction = 8'''
        else:
            direction = 0

        ser.write(chr(direction))
        pygame.display.update()

pygame.quit()
quit()