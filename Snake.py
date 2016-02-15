import pygame, sys, random
from pygame.locals import *
from random import randrange
pygame.init()

Bialy = (255, 255, 255)

#--okno--
roz = 10
wys = 400
sze = 400
okno = pygame.display.set_mode((sze, wys), 0, 32)
pygame.display.set_caption('Snake')
font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 24)

#--tekst na srodku--
def tekst(tresc):
    tekst = font.render(tresc, True, Bialy)
    ramka = tekst.get_rect()
    ramka.center = (int(sze/2 - roz), int(wys/2 - roz))
    okno.blit(tekst, ramka)
    pygame.display.update()

def pauza():
    P = True
    tekst('Nacisnij enter')
    while P == True:
        for event in pygame.event.get():

                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()
                    
                if event.type == KEYDOWN and event.key == K_RETURN:
                    P = False
                    okno.fill((0,0,0))
    
#--menu--
G = False 
while True:
    
    #--poczatek--
    x = int(sze/2 - roz)
    y = int(wys/2 - roz)
        
    #--waz--
    dlug = 4 
    waz = [0] * dlug
    for i in range(dlug):
        waz[i] = [0] * 2
            
    for i in range(dlug):
        waz[i][0] = x
        waz[i][1] = y
        
    tekst('Naciśnij enter aby rozpocząć')
    
    for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
                
            if event.type == KEYDOWN and event.key == K_RETURN:
                G = True
    #--gra--
    R = 1
    P = True
    while G == True:
        okno.fill((0,0,0))
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_UP and R != 1:
                    R = 0
                elif event.key == K_DOWN and R != 0:
                    R = 1
                elif event.key == K_RIGHT and R != 3:
                    R = 2
                elif event.key == K_LEFT and R != 2:
                    R = 3
                elif event.key == K_p:
                    pauza()

        #--zmiana kierunku--
        if R == 0: waz[0][1] = waz[0][1] - roz
        if R == 1: waz[0][1] = waz[0][1] + roz
        if R == 2: waz[0][0] = waz[0][0] + roz
        if R == 3: waz[0][0] = waz[0][0] - roz

        #--porazka--
        if waz[0][0] < 0 or waz[0][0] > sze-10 or waz[0][1] < 0 or waz[0][1] > sze-10:
            G = False
        for i in range(1, dlug):
            if waz[0][0] == waz[i][0] and waz[0][1] == waz[i][1]:
                G = False

        #--punkty--
        if P == True:
            xz = randrange(0, sze, roz)
            yz = randrange(0, wys, roz)
            P = False
        
        if waz[0][0] == xz and waz[0][1] == yz:
            P = True
            for i in range(2):
                dlug += 1
                waz.append([0]*2)
                waz[dlug-1][0] = waz[dlug-2][0]
                waz[dlug-1][1] = waz[dlug-2][1]

        #--rysowanie weza--
        for i in range(dlug):
            pygame.draw.rect(okno, Bialy, (waz[i][0], waz[i][1], roz, roz), 1)

        #--przesuwanie tablicy--
        for i in range(dlug - 1, 0, -1):
            waz[i][0] = waz[i - 1][0]
            waz[i][1] = waz[i - 1][1]

        pygame.draw.rect(okno, Bialy, (xz, yz, roz, roz), 1)    
        pygame.display.update()
        pygame.time.delay(100)
    
