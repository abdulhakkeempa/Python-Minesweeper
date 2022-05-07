from random import randint
import numpy as np
import pygame,sys
from pygame import mixer

#10x10 minesweeper
pygame.init()
mixer.init()

#global variables
clicks = 0
oldClick = 0
minesFound = 0
oldMines = 0

#rgb - color code
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,100,0)

#screen settings.
screen = pygame.display.set_mode((500,600))
screen.fill(WHITE)
pygame.display.set_caption("Mine Sweeper")

#loading - required fonts
font = pygame.font.SysFont("Arial",24)
resultFont = pygame.font.SysFont("Times new Roman",30)

#loading - required images
imageMine = pygame.image.load("images\mine2.png")
imageCross = pygame.image.load("images\cross.png")

#array for the mine board.
consoleBoard = np.zeros((10,10))

#draw board lines
def drawLines():
    for i in range(50,500,50):
        pygame.draw.line(screen,BLACK,(i,0),(i,500),5)
        pygame.draw.line(screen,BLACK,(0,i),(500,i),5)

#restart function
def restart():
    global clicks,minesFound
    screen.fill(WHITE)
    screen.blit(infoText,(45,555))
    drawLines()
    plantMines()
    clicks = 0
    minesFound = 0

#function to display click count
def displayClicks():
    global oldClick
    coveringText = font.render(f"Clicks : {oldClick} / 10",True,WHITE)
    screen.blit(coveringText,(370,510))
    clickText = font.render(f"Clicks : {clicks} / 10",True,BLACK)
    screen.blit(clickText,(370,510))
    oldClick = clicks

#function to display mine count
def displayMinesCount():
    global oldMines
    coveringText = font.render(f"Mines : {oldMines} / 7",True,WHITE)
    screen.blit(coveringText,(250,510))
    mineText = font.render(f"Mines : {minesFound} / 7",True,BLACK)
    screen.blit(mineText,(250,510))
    oldMines = minesFound

#function to randomly place mines.
def plantMines():
    for i in range(10):
        for j in range(10):
            consoleBoard[i][j]=0
    
    for i in range(7):
        consoleBoard[randint(0,9)][randint(0,9)] = 1

#function for beep sounds.
def beepSound(condition):
    if condition==1:
        mixer.music.load("sound\correctBeep.wav")
        mixer.music.play()
    elif condition==2:
        mixer.music.load("sound\wrongBeep.wav")
        mixer.music.play()  
    elif condition==-1:
        mixer.music.load("sound\FailedBeep.wav")
        mixer.music.play()               
    elif condition==0:
        mixer.music.load("sound\wonBeep.wav")
        mixer.music.play()         

#invoking functions
drawLines()
plantMines()

#description text
STRING = " FIND 7 HIDDEN MINES WITHIN 10 CLICKS "
infoText = font.render(STRING,True,WHITE,BLACK)
screen.blit(infoText,(45,555))

#reset button
reset = resultFont.render("  Reset  ",True,BLACK,RED)
resetRect = reset.get_rect()
resetRect.center = (60,525)

#failed and win announcments.
failed = resultFont.render(" Failed ",True,WHITE,RED)
failedRect = failed.get_rect()
failedRect.center = (180,525)

win = resultFont.render(" Won ",True,WHITE,GREEN)
winRect = win.get_rect()
winRect.center = (180,525)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and clicks<10 and event.pos[1]<=500:
            clicks = clicks+1
            # print(clicks)
            pos = pygame.mouse.get_pos()
            x = pos[0]//50
            y = pos[1]//50
            if consoleBoard[y][x]==1:
                screen.blit(imageMine,(x*50,y*50))
                minesFound=minesFound+1
                beepSound(1)
                if minesFound==7:
                    screen.blit(win,winRect)
                    beepSound(0)
            else:
                beepSound(2)
                screen.blit(imageCross,(x*50,y*50))
        if event.type==pygame.MOUSEBUTTONDOWN and clicks>=10 and minesFound!=7 and event.pos[1]<500:
            beepSound(-1)
            screen.blit(failed,failedRect)
        if (event.type == pygame.KEYDOWN and pygame.K_r) or (event.type==pygame.MOUSEBUTTONDOWN and event.pos[1]>500 and event.pos[0]<120):
            restart()
    screen.blit(reset,resetRect)
    displayMinesCount()
    displayClicks()
    pygame.display.update()

