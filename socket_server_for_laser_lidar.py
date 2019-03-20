#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
import pygame
from pygame.locals import *

import json

pygame.init()
screen = pygame.display.set_mode((1024,768), 0, 32)
pygame.display.set_caption("Laser Lidar")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

def echo_handler(address, client_sock):
    msg=""
    print('Got connection from {}'.format(address))
    while True:
        msg = msg+client_sock.recv(8192).decode('utf-8')
        #print(msg)
        flagstr=msg.find('}{')
        #print(flagstr)
        if flagstr <0:
            continue

        tmpstr = msg[0:flagstr+1]
        msg=msg[flagstr+1:len(msg)]
        print(tmpstr)

        data = json.loads(tmpstr)
        data=data['data']

        for i in range(len(data)):
            print(data[i]['degree'], data[i]['dist'])
            return data[i]['degree'], data[i]['dist']
            pygame.draw.circle(background, (255, 0, 0), (int(data[i]['degree']), int(data[i]['dist'])), 2)

    client_sock.close()

def main(address, backlog=10):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)

    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)

if __name__ == '__main__':
    main(('', 20002))
    screen.blit(background,(0, 0))
    pygame.display.flip()