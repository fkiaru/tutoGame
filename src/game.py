import sys
import pygame
from pygame.locals import *
import brain as logic

# CONSTANTS
GREY = pygame.Color(128, 128, 128)
BLACK = (0, 0, 0)
WHITE = pygame.Color(255, 255, 255)   # White
BLUE = pygame.Color(0, 0, 255)   
RED = pygame.Color(255, 0, 0) 
XDIM = 400
YDIM = 400

# Initialize game
pygame.init()
pygame.display.set_caption("Minesweeper")
DISPLAYSURF = pygame.display.set_mode((XDIM, YDIM)) 
FramePerSec = pygame.time.Clock()
FPS = 50
DISPLAYSURF.fill(GREY)
MINE_IMG = pygame.image.load("resources/mine.png")
prevhitlist = []
mines = []

def drawboardlines(DISPLAYSURF, XDIM, YDIM):
    i = 0
    while i <= XDIM:
        pygame.draw.line(DISPLAYSURF, BLACK, (0,i), (XDIM, i))   # For horizontal line
        pygame.draw.line(DISPLAYSURF, BLACK, (i,0), (i, YDIM))   # For vertical line
        i += 40


drawboardlines(DISPLAYSURF, XDIM, YDIM)

def clearcells(cell):
    x,y=cell
    for ax,ay in ((x+1,y),(x-1,y),(x,y+1),(x,y-1),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1)):
        prevhitlist.append((ax,ay))
        if ax>=0 and ax <=9 and ay>=0 and ay <=9 and (x,y) not in prevhitlist:
            if (ax,ay) in mines:
                i = 1
                while i < 40:
                    pygame.draw.line(DISPLAYSURF, BLUE, ((ax*40)+1,(ay*40)+i),((ax*40)+39,(ay*40)+i))
            else:
                i = 1
                while i < 40:
                    pygame.draw.line(DISPLAYSURF, WHITE, ((ax*40)+1,(ay*40)+i),((ax*40)+39,(ay*40)+i))
                    i += 1
            prevhitlist.append((x,y))
    pygame.display.update()

def changecolor(cell, HIT):    #HIT : If HIT BOMB
    x,y = cell
    x = x*40
    y=y*40
    i = 1
    # while i < 40:
    #     pygame.draw.line(DISPLAYSURF, WHITE, (x+1,y+i),(x+39,y+i))
    #     i += 1
    if HIT: # Hit a bomb
        while i < 40:
            pygame.draw.line(DISPLAYSURF, RED, (x+1,y+i),(x+39,y+i))
            i += 1
        rect = MINE_IMG.get_rect()
        rect.center = (x+20,y+20)
        #DISPLAYSURF.blit(MINE_IMG, rect)
        i=1
    else:   #Clear up all 6 cells
        while i < 40:
            pygame.draw.line(DISPLAYSURF, WHITE, (x+1,y+i),(x+39,y+i))
            i += 1
        pass


if __name__ == "__main__":

    mines = []
    matrix = [[0 for x in range(10)] for y in range(10)]
    debug = 1
    mines = logic.placement(debug,matrix,mines)
    matrix = logic.numbering(matrix,mines)
    # Game loop
    while True:
        for event in pygame.event.get():    #pygame.event.get gets the event done by the user (mouse scroll, click, type etc)
            if event.type == QUIT:  #If we attempt to guit the game, the game quits.
                pygame.quit()   #Closes the pygame window
                sys.exit()      # Closes the python script
            if event.type == MOUSEBUTTONDOWN:
                xcoord,ycoord = pygame.mouse.get_pos()
                x = xcoord//40
                y = ycoord//40
                cell = (x,y)
                if (cell in prevhitlist) and cell not in mines:
                    pygame.display.set_caption("HIT SOMEWHERE ELSE")
                else:
                    prevhitlist.append(cell)
                    if cell in mines:
                        changecolor(cell,1)  # Hit mine
                        #showscore(prevhitlist)
                    else:
                        changecolor(cell,0)  # Missed mine
                        clearcells(cell)
                    if pygame.display.get_caption()[0] == "HIT SOMEWHERE ELSE":
                        pygame.display.set_caption("Minesweeper") 
            pygame.display.update()
            FramePerSec.tick(FPS)   #Setting the frame rate of 60fps