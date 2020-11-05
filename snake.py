#!/usr/bin/env python

#Author: James Stallworthy
#Date: 02/11/2020

import random
import time
import pygame

class Grid:
    def __init__(self):
        self.respawnFood()
 
    def respawnFood(self):
        self.foodPos = [random.randint(0,_horTiles-1),random.randint(0,_vertTiles-1)]
        if self.foodPos in _snake.bodyPositions:
            self.respawnFood()

    def draw(self):
        #draw food
        pygame.draw.rect(_screen,(0,255,0),(self.foodPos[0]*_tileSize,self.foodPos[1]*_tileSize,_tileSize,_tileSize))
        #draw horizontal grid
        for x in range(_horTiles):
            pygame.draw.line(_screen,(0,0,0),(0,x*_tileSize,), (_screenHeight,x*_tileSize))
         #draw veritcal grid
        for x in range(_vertTiles):
            pygame.draw.line(_screen,(0,0,0),(x*_tileSize, 0), (x*_tileSize,_screenHeight))

class Snake:
    def __init__(self):
        self.bodyPositions = [[5,5],[6,5],[7,5]]
        self.XVelocity = -1
        self.YVelocity = 0
        self.inputThisFrame = False

    def getPositions(self):
        return self.bodyPositions

    def draw(self):
        for point in self.bodyPositions:
            pygame.draw.rect(_screen,(255,0,0),(point[0]*_tileSize,point[1]*_tileSize,_tileSize,_tileSize))

    def updateDirection(self, keyPressEvent):
        #stop multiple inputs per frame
        if self.inputThisFrame == False:
            if keyPressEvent.key == pygame.K_UP and self.YVelocity == 0:
                self.XVelocity = 0
                self.YVelocity = -1
                self.inputThisFrame = True
            elif keyPressEvent.key == pygame.K_DOWN and self.YVelocity == 0:
                self.XVelocity = 0
                self.YVelocity = 1
                self.inputThisFrame = True
            elif keyPressEvent.key == pygame.K_LEFT and self.XVelocity == 0:
                self.XVelocity = -1
                self.YVelocity = 0
                self.inputThisFrame = True
            elif keyPressEvent.key == pygame.K_RIGHT and self.XVelocity == 0:
                self.XVelocity = 1
                self.YVelocity = 0
                self.inputThisFrame = True

    def update(self, grid):
        newBodyPart = [self.bodyPositions[0][0]+self.XVelocity, self.bodyPositions[0][1]+self.YVelocity]
        global _gameOver
        global _speed
        #Check for body hit
        if newBodyPart in self.bodyPositions[1:]:
            _gameOver = True

        #Wrapping
        if newBodyPart[0] < 0:
            newBodyPart[0] = _horTiles-1

        elif newBodyPart[0] >= _horTiles:
            newBodyPart[0] = 0

        elif newBodyPart[1] < 0:
            newBodyPart[1] = _vertTiles-1

        elif newBodyPart[1] >= _vertTiles:
            newBodyPart[1] = 0

        self.bodyPositions.insert(0, newBodyPart)

        #Growing snake
        if grid.foodPos == self.bodyPositions[0]:
            grid.respawnFood()
            _speed = _speed + 1
        else:
            self.bodyPositions.pop()

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


_screenHeight = 500
_screenWidth = 500
_tileSize = 50
_horTiles = int(_screenHeight / _tileSize)
_vertTiles = int(_screenWidth / _tileSize)

pygame.init()

pygame.display.set_caption('Snake')
_screen = pygame.display.set_mode([_screenHeight,_screenWidth])

_fontSize = 50
_font = pygame.font.Font("./OpenSans-Bold.ttf",_fontSize)
_running = True
_gameOver = False

_snake = Snake()
_grid = Grid()
_speed = 4

while _running:
    _snake.inputThisFrame = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
        if event.type == pygame.KEYDOWN:
            _snake.updateDirection(event)

    _snake.update(_grid)

    _screen.fill((255,255,255))

    _snake.draw()
    _grid.draw()

    TextSurf, TextRect = text_objects("Score: " + str(len(_snake.bodyPositions) - 3),_font)
    TextRect.center = ((_screenWidth/2),_fontSize/2)
    _screen.blit(TextSurf,TextRect)

    pygame.display.flip()
    time.sleep(1/_speed)
    if _gameOver:
        _running = False

#Game over text
if _gameOver:
    TextSurf, TextRect = text_objects("Game Over!",_font)
    TextRect.center = ((_screenWidth/2),(_screenHeight/2))
    _screen.blit(TextSurf,TextRect)
    pygame.display.flip()
    time.sleep(5)

pygame.quit()
