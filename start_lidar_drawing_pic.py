#!/usr/bin/env python
import serial
import matplotlib as plt
import math 
import pygame
from pygame.locals import *
from sys import exit


# instance a ser object
pygame.init()
ser = serial.Serial("/dev/ttyS0",230400, timeout=30)
screen = pygame.display.set_mode((1024,768),0,32)


# turn on the lidar
ser.write(b'b')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    sync = ser.read(1)
    if sync and sync[0] == 0xfa:
        datalist = []
        data = ser.read(41)
        angle = (data[0]- 0xa0)*6 
        #print(angle) 
        for i in range(0,6):
            distance = (data[6+6*i] * 0xff + data[5+6*i])
            x = distance * math.cos(angle) 
            y = distance * math.sin(angle)
            print("x: %f,y: %f" % (x,y))
            """
            try: 
                with open("data.txt", 'a') as f:
                    f.write(str(x))
                    f.write(",")
                    f.write(str(y))
                    f.write('\n')

            except Exception as e:
                print(e)
                """
            screen.set_at((int(x)+512, int(y)+384),(255,0,0))
            pygame.display.update()


