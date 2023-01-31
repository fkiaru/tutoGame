import sys
import pygame
from pygame.locals import *
import time
import brain as logic

# CONSTANTS
BLACK = (0, 0, 0)
GREEN = pygame.Color(0,255,0)
GREY = pygame.Color(128, 128, 128)
WHITE = pygame.Color(255, 255, 255)   # White
BLUE = pygame.Color(0, 0, 255)   
RED = pygame.Color(255, 0, 0) 
XDIM = 400
YDIM = 400

# Initialize game
pygame.init()
pygame.display.set_caption("Minesweeper")
DISPLAYSURF = pygame.display.set_mode((XDIM, YDIM),pygame.SCALED) 
FramePerSec = pygame.time.Clock()
FPS = 50
DISPLAYSURF.fill(GREY)
MINE_IMG = pygame.image.load("resources/mine.png")
font = pygame.font.SysFont("Verdana", 20)
prevhitlist = set()
mines = []
Winner = -1

def drawboardlines(DISPLAYSURF, XDIM, YDIM, Color):
    i = 0
    while i <= XDIM:
        pygame.draw.line(DISPLAYSURF, Color, (0,i), (XDIM, i))   # For horizontal line
        pygame.draw.line(DISPLAYSURF, Color, (i,0), (i, YDIM))   # For vertical line
        i += 40


def changecellcolor(cell, color):   #Single cell change color to 'color'
    x,y = cell
    i = 1
    while i < 40:
        pygame.draw.line(DISPLAYSURF, color, ((x*40)+1,(y*40)+i),((x*40)+39,(y*40)+i))
        i += 1


def clearcells(cell):   #Clear cells around central
    x,y=cell
    for ax,ay in ((x+1,y),(x-1,y),(x,y+1),(x,y-1),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1)):
        if ax>=0 and ax <=9 and ay>=0 and ay <=9:
            if (ax,ay) in prevhitlist:
                continue
            else:
                if (ax,ay) in mines:
                    changecellcolor((ax,ay),BLUE)
                else:
                    changecellcolor((ax,ay), WHITE)
                    value = font.render(str(matrix[ax][ay]), True, BLACK)
                    DISPLAYSURF.blit(value, ((ax*40)+11,(ay*40)+11))
                prevhitlist.add((ax,ay))

if __name__ == "__main__":

    drawboardlines(DISPLAYSURF, XDIM, YDIM, BLACK)
    mines = []
    matrix = [[0 for x in range(10)] for y in range(10)]
    debug = 0
    mines = logic.placement(debug,matrix,mines)
    matrix = logic.numbering(matrix,mines)
    curscore = 0
    mouse_pressed = False
    press_time = time.time()
    # Game loop
    while True:
        scores = font.render(str(curscore), True, BLACK)
        #DISPLAYSURF.blit(scores, (10,10))
        for event in pygame.event.get():    #pygame.event.get gets the event done by the user (mouse scroll, click, type etc)
            if event.type == QUIT:  #If we attempt to guit the game, the game quits.
                pygame.quit()   #Closes the pygame window
                sys.exit()      # Closes the python script

            elif event.type == MOUSEBUTTONDOWN:
                xcoord,ycoord = pygame.mouse.get_pos()
                x = xcoord//40
                y = ycoord//40
                cell = (x,y)
                if len(prevhitlist) == 0 and cell in mines: # So that person doesn't die on first chance
                    mines = logic.placement(debug,matrix,mines)
                    matrix = logic.numbering(matrix,mines)

                if event.button == 3:
                    changecellcolor(cell,BLUE)
                    prevhitlist.add(cell)
                else:
                    if (cell in prevhitlist) and cell not in mines:
                        pygame.display.set_caption("HIT SOMEWHERE ELSE")
                    else:
                        prevhitlist.add(cell)
                        if cell in mines:
                            changecellcolor(cell,RED)  # Hit mine
                            Winner = 0
                            #showscore(prevhitlist)
                        else:
                            changecellcolor(cell,WHITE)  # Missed mine
                            value = font.render(str(matrix[x][y]), True, BLACK)
                            DISPLAYSURF.blit(value, ((x*40)+11,(y*40)+10))
                            clearcells(cell)
                        if pygame.display.get_caption()[0] == "HIT SOMEWHERE ELSE":
                            pygame.display.set_caption("Minesweeper") 
                if set(mines).issubset(prevhitlist):
                    Winner = 1

            if Winner == 1:
                pygame.display.set_caption("WINNER")
                drawboardlines(DISPLAYSURF, XDIM, YDIM, GREEN)
                pygame.display.update()
                time.sleep(5)
                pygame.quit()   #Closes the pygame window
                sys.exit()      # Closes the python script
            
            elif Winner == 0:
                pygame.display.set_caption("LOSER")
                drawboardlines(DISPLAYSURF, XDIM, YDIM, RED)
                pygame.display.update()
                time.sleep(5)
                pygame.quit()   #Closes the pygame window
                sys.exit()      # Closes the python script

            pygame.display.update()
            FramePerSec.tick(FPS)   #Setting the frame rate of 60fps