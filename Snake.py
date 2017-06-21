import pygame, sys, random
from pygame.locals import *
from random import randrange
pygame.init()

White = (255, 255, 255)

#--window--
size = 10
width = 400
height = 400
hScreen = 500
window = pygame.display.set_mode((width, hScreen), 0, 32)
pygame.display.set_caption('Snake')
font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 24) 

#--clean screen--
def clean():
    window.fill((0,0,0))
    pygame.display.update()

    
#--menu--
G = False 
while True:
    
    #--start--
    x = int(width/2 - size)
    y = int(height/2 - size)
        
    #--snake--
    length = 4 
    snake = [0] * length
    for i in range(length):
        snake[i] = [0] * 2
            
    for i in range(length):
        snake[i][0] = x
        snake[i][1] = y
    
    for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
                
            if event.type == KEYDOWN and event.key == K_RETURN:
                G = True
    #--game--          
    R = 1
    P = True
    while G == True:
        clean()
        B = False
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_UP and R != 1 and B == False:
                    R = 0
                    B = True
                if event.key == K_DOWN and R != 0 and B == False:
                    R = 1
                    B = True
                if event.key == K_RIGHT and R != 3 and B == False:
                    R = 2
                    B = True
                if event.key == K_LEFT and R != 2 and B == False:
                    R = 3
                    B = True
                if event.key == K_p:
                    pauza()

        #--control--
        if R == 0: snake[0][1] = snake[0][1] - size
        if R == 1: snake[0][1] = snake[0][1] + size
        if R == 2: snake[0][0] = snake[0][0] + size
        if R == 3: snake[0][0] = snake[0][0] - size

        #--fail--
        if snake[0][0] < 0 or snake[0][0] > width-10 or snake[0][1] < 0 or snake[0][1] > width-10:
            G = False
        for i in range(1, length):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                G = False

        #--points--
        if P == True:
            xz = randrange(0, width, size)
            yz = randrange(0, height, size)
            P = False
        
        if snake[0][0] == xz and snake[0][1] == yz:
            P = True
            for i in range(2):
                length += 1
                snake.append([0]*2)
                snake[length-1][0] = snake[length-2][0]
                snake[length-1][1] = snake[length-2][1]

        #--draw snake--
        for i in range(length):
            pygame.draw.rect(window, White, (snake[i][0], snake[i][1], size, size), 1)

        #--move--
        for i in range(length - 1, 0, -1):
            snake[i][0] = snake[i - 1][0]
            snake[i][1] = snake[i - 1][1]

        pygame.draw.rect(window, White, (xz, yz, size, size), 1)    
        pygame.display.update()
        pygame.time.delay(100)
