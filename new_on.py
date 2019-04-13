#!/usr/bin/env python
import serial
import matplotlib as plt
import math 
import time 
import pygame
from pygame.locals import *
from sys import exit

# instance a ser object
pygame.init()
ser = serial.Serial("/dev/ttyS0",230400, timeout=30)
screen = pygame.display.set_mode((1920,1080),0,32)
Pi = 3.1415926535897

# turn on the lidar
ser.write(b'b')
try:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        sync = ser.read(1)
        if sync and sync[0] == 0xfa:
            datalist = []
            data = ser.read(41)
            for i in range(0,6):
                distance = (data[6+6*i] * 0xff + data[5+6*i])
                angle = (2 * Pi * (data[0]- 0xa0)*6 + i) / 360.0 
                #print(type(data[0] - 0xa0))
                angle = 2*Pi*((data[0]- 0xa0)*6 + i ) / 360.0
                x = distance * math.cos(angle) 
                y = distance * math.sin(angle)

                screen.set_at((int(x)+960, int(y)+540),(0,255,0))
                pygame.display.update()
                print("x: %f,y: %f" % (x,y))
                print("angle: %f,distance: %f" % (angle,distance))
                try: 
                    with open("data.txt", 'a') as f:
                        current_time = time.localtime()
                        time_str = time.strftime("%H:%M:%S", current_time)
                        f.write(time_str)
                        f.write(",")
                        f.write('angle:')
                        f.write(str(angle))
                        f.write(",")
                        f.write('Distance:')
                        f.write(str(distance))
                        f.write(",")
                        f.write('x:')
                        f.write(str(x))
                        f.write(",")
                        f.write('y:')
                        f.write(str(y))
                        f.write('\n')
                except Exception as e:
                    print(e)
except KeyboardInterrupt as e:
    ser.write(b'e')
    ser.close()
    print("Turn of lidar, quit")

