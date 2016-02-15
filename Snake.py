import pygame, sys, random
from pygame.locals import *
from random import randrange
pygame.init()

#--okno--
roz = 10
wys = 400
sze = 800
okno = pygame.display.set_mode((sze, wys), 0, 32)
pygame.display.set_caption('Snake')

#--poczatek--
x = int(sze/2 - roz)
y = int(wys/2 - roz)
pygame.draw.rect(okno, (255, 255, 255), (x, y, roz, roz), 1)
pygame.display.update()

#--waz--
dlug = 4 
waz = [0] * dlug
for i in range(dlug):
    waz[i] = [0] * 2
        
for i in range(dlug):
    waz[i][0] = x
    waz[i][1] = y 

#--gra--
R = 1
Punkt = True
input()
while True:
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_UP and R != 1:
                R = 0
            elif event.key == K_DOWN and R != 0:
                R = 1
            elif event.key == K_RIGHT and R != 3:
                R = 2
            elif event.key == K_LEFT and R != 2:
                R = 3

    if R == 0: waz[0][1] = waz[0][1] - roz
    if R == 1: waz[0][1] = waz[0][1] + roz
    if R == 2: waz[0][0] = waz[0][0] + roz
    if R == 3: waz[0][0] = waz[0][0] - roz

    if Punkt == True:
        xz = randrange(0, sze, roz)
        yz = randrange(0, wys, roz)
        Punkt = False
    
    if waz[0][0] == xz and waz[0][1] == yz:
        Punkt = True
        for i in range(2):
            dlug += 1
            waz.append([0]*2)
            waz[dlug-1][0] = waz[dlug-2][0]
            waz[dlug-1][1] = waz[dlug-2][1]
            
    okno.fill((0,0,0))
    
    for i in range(dlug):
        pygame.draw.rect(okno, (255, 255, 255), (waz[i][0], waz[i][1], roz, roz), 1)

    for i in range(dlug - 1, 0, -1):
        waz[i][0] = waz[i - 1][0]
        waz[i][1] = waz[i - 1][1]

    pygame.draw.rect(okno, (255, 255, 255), (xz, yz, roz, roz), 1)    
    pygame.display.update()
    pygame.time.delay(100)
    
