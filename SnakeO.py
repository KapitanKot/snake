import pygame
import sys
import random
from pygame.locals import *
from random import randrange, randint

class Game(object):
    '''App'''
    
    def __init__(self, width = 40, height = 40, size = 10):
        
        pygame.init()
        self.started = False
        self.reset = False
        self.board = Board(width * size, height * size)
        self.snake = Snake(width * size, height * size, size)
        self.point = Points(width * size, height * size, size)
        self.clock = pygame.time.Clock()
        self.bonus = False
        self.tick = 0

    def events(self):
        '''Event handler'''
        
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_RETURN:
                self.started = True
                
            if event.type == KEYDOWN and self.started == True:
                self.snake.keys()
                
            if event.type == KEYDOWN and event.key == K_p:
                self.started = False

            if event.type == KEYDOWN and event.key == K_r:
                self.snake.reset()
                self.reset = True
                self.board.score = 0
                self.bonus = False
                self.started = False

    def get_point(self):

        if self.snake.cobra[0][0] == self.point.px and self.snake.cobra[0][1] == self.point.py:
            self.point.alive = False
            self.snake.grow()
            self.board.score += 1

    def get_bonus(self):
        
        if self.snake.cobra[0][0] == self.point.bx and self.snake.cobra[0][1] == self.point.by:
            self.point.bonus = False
            self.bonus = False
            self.snake.grow(3)
            self.board.score += 3

    def counter(self):

        if self.reset:
            self.tick = 0
            self.bonus = False
        if self.started:
            self.tick += 1
            if self.tick == 90:
                if randint(0,100) < 100:
                    self.bonus = True
                else:
                    self.tick = 0
            if self.tick == 150:
                self.bonus = False
                self.point.bonus_alive = False
                self.tick = 0
    
    def run(self):
        '''Run game'''

        while not self.events():
            
            self.board.draw_board(self.snake, self.point, self.started, self.reset, self.bonus)
            self.get_point()
            self.get_bonus()

            if self.reset:
                self.reset = False
                self.point.bonus_alive = False
            if self.started:
                if self.snake.move() == False:
                    self.snake.reset()
                    self.reset = True
                    self.board.score = 0
                    self.started = False
            self.clock.tick(12)
            self.counter()
            
                
class Board(object):
    
    def __init__(self, width, height):
        '''Window'''
        
        self.width = width
        self.height = height
        self.score = 0
        self.window = pygame.display.set_mode((self.width, self.height + 18), 0, 32)
        self.font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 12)
        self.text = self.font.render('Start (Enter)      Pause (P)       Restart (R)', True, (255, 255, 255))
        self.score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))

        pygame.display.set_caption('Snake')
        self.start = False

    def draw_board(self, *args):
        '''Draw elements'''

        if args[3]:
            self.start = False
        elif args[2]:
            self.start = True
        
        background = (0, 0, 0)
        self.window.fill(background)
        pygame.draw.rect(self.window, (255, 255, 255), (0, self.height+1, self.width, 3), 1)

        self.score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.window.blit(self.text, (1, self.height+4))
        self.window.blit(self.score_text, (self.width - 80, self.height+4))

        args[0].draw_snake(self.window)
        if args[3]:
            args[1].draw_point(self.window, True)
        if self.start:
            args[1].draw_point(self.window)
            if args[4]:
                args[1].draw_bonus(self.window)


        pygame.display.update()

class Points(object):
    '''Points'''

    def __init__(self, width, height, size):

        self.width = width
        self.height = height
        self.size = size
        self.px = 0
        self.py = 0
        self.bx = 0
        self.by = 0
        self.alive = False
        self.bonus_alive = False
        self.cherry = pygame.image.load('Cherry.bmp')

    def draw_point(self, surface, reset=False):
        '''Draw point in random place'''

        if reset:
            self.alive = False
        if self.alive == False:
            self.px = randrange(0, self.width, self.size)
            self.py = randrange(0, self.height, self.size)
            self.alive = True
        if reset is False:
            pygame.draw.rect(surface, (255, 255, 255), (self.px, self.py, self.size, self.size), 1)

    def draw_bonus(self, surface):

        if self.bonus_alive == False:
            self.bx = randrange(0, self.width, self.size)
            self.by = randrange(0, self.height, self.size)
            self.bonus_alive = True

        surface.blit(self.cherry, (self.bx, self.by))    
        #pygame.draw.rect(surface, (0, 255, 255), (self.bx, self.by, self.size, self.size), 1)

class Snake(object):

    def __init__(self, width, height, size):
        
        self.startx = int(width/2 - size)
        self.starty = int(height/2 - size)
        self.width = width
        self.height = height
        self.size = size
        self.way = 0
        self.length = 4
        self.cobra = self.new()

    def keys(self):
        '''Control'''

        key = pygame.key.get_pressed()
        if key[273] and self.way != 1:
            self.way = 0
        if key[274] and self.way != 0:
            self.way = 1
        if key[275] and self.way != 3:
            self.way = 2
        if key[276] and self.way != 2:
            self.way = 3
        
    def new(self):
        '''Create snake'''
        
        self.length = 4
        snake = [0] * self.length
        for i in range(self.length):
            snake[i] = [0] * 2
            snake[i][0] = self.startx
            snake[i][1] = self.starty
            
        return snake

    def grow(self, x=1):

        for i in range(x):
            self.cobra.append([self.cobra[-1][0], self.cobra[-1][1]])
            self.length += 1

    def reset(self):
        '''Draw snake in start point'''
        
        self.way = 0
        self.cobra = self.new()
    
    def move(self):
        '''Move'''
        
        if self.way == 0: self.cobra[0][1] = self.cobra[0][1] - self.size
        if self.way == 1: self.cobra[0][1] = self.cobra[0][1] + self.size
        if self.way == 2: self.cobra[0][0] = self.cobra[0][0] + self.size
        if self.way == 3: self.cobra[0][0] = self.cobra[0][0] - self.size

        #fail
        if self.cobra[0][0] < 0 or self.cobra[0][0] > self.width-self.size or self.cobra[0][1] < 0 or self.cobra[0][1] > self.width-self.size:
            return False
        for i in range(1, self.length):
            if self.cobra[0][0] == self.cobra[i][0] and self.cobra[0][1] == self.cobra[i][1]:
                return False
            
        for i in range(self.length-1, 0, -1):
            self.cobra[i][0] = self.cobra[i - 1][0]
            self.cobra[i][1] = self.cobra[i - 1][1]

    def draw_snake(self, surface):
        for i in range(self.length):
            pygame.draw.rect(surface, (255, 255, 255), (self.cobra[i][0], self.cobra[i][1], self.size, self.size), 1)

        
if __name__ == '__main__':
    game = Game(40, 40)
    game.run()
