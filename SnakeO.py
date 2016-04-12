import pygame, sys, random
from pygame.locals import *
from random import randrange

class Game(object):
    """Main"""
    
    def __init__(self, width = 40, height = 40, size = 10):
        pygame.init()
        self.started = False
        self.board = Board(width * size, height * size)
        self.snake = Snake(width * size, height * size, size)
        self.clock = pygame.time.Clock()

    def events(self):
        """Event handler"""
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
                self.started = False

    def run(self):
        """Main loop"""
        while not self.events():
            self.board.draw(self.snake)
            if self.started:
                if self.snake.move() == False:
                    self.snake.reset()
                    self.started = False
            self.clock.tick(12)
            
class Board(object):
    
    def __init__(self, width, height):
        """Window"""
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height + 18), 0, 32)
        font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 12)
        self.text = font.render('Start (Enter)      Pause (P)      Restart (R)', True, (255, 255, 255))
        pygame.display.set_caption('Snake')

    def draw(self, *args):
        """Draw elements"""
        background = (0, 0, 0)
        self.window.fill(background)
        pygame.draw.rect(self.window, (255, 255, 255), (0, self.height+1, self.width, 3), 1)
        self.window.blit(self.text, (1, self.height+4))
        for arg in args:
            arg.drawSnake(self.window)
            
        pygame.display.update()

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
        '''Create default snake'''
        self.length = 4
        snake = [0] * self.length
        for i in range(self.length):
            snake[i] = [0] * 2
            snake[i][0] = self.startx
            snake[i][1] = self.starty
        return snake

    def reset(self):
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

    def drawSnake(self, surface):
        for i in range(self.length):
            pygame.draw.rect(surface, (255, 255, 255), (self.cobra[i][0], self.cobra[i][1], self.size, self.size), 1)

        
if __name__ == "__main__":
    game = Game(40, 40)
    game.run()
