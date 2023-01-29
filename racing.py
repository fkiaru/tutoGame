'''
IMPORTANT NOTES
- (0,0) is the topleft point on screen
- Rect (Box around image) and the image itself don't move together if not correctly coded
'''

# importing packages
import sys
import time
import random
import pygame
from pygame.locals import *

# Constants declarations
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
color1 = pygame.Color(0, 0, 0)         # Black
color2 = pygame.Color(255, 255, 255)   # White
color3 = pygame.Color(128, 128, 128)   # Grey
color4 = pygame.Color(255, 0, 0)       # Red
FPS = 20
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
  
# Initialize Game
pygame.init()  #Init function intializes the pygame engine. Line must be included before any code is written
DISPLAYSURF = pygame.display.set_mode((400,600)) 
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
FramePerSec = pygame.time.Clock()

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("./resources/AnimatedStreet.png")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./resources/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite): #Player is a child class of Sprite
    def __init__(self):
        super().__init__()          # Calls the init function of the sprite class
        self.image = pygame.image.load("./resources/Player.png") 
        self.rect = self.image.get_rect()   # Defines the collide borders 
        self.rect.center = (160, 520)       # Defines starting position for Rect
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:  # Makes sure player doesn't move off the screen
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)  # Moves the rect by 5 to the left
        if self.rect.right < SCREEN_WIDTH:  # To make sure player doesn't move to the right of the screen
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
         
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups for making it easier to deal with all of them together
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1) # Adds a sprite into the sprite group
all_sprites.add(E1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  #This object INC_SPEED is called every 1000ms or 1s

# Game loop
while True: #This makes the game window run again and again.

    for event in pygame.event.get():    #pygame.event.get gets the event done by the user (mouse scroll, click, type etc)
        if event.type == INC_SPEED: # If inc_speed event is called, games becomes faster
            SPEED +=2
        if event.type == QUIT:  #If we attempt to guit the game, the game quits.
            pygame.quit()   #Closes the pygame window
            sys.exit()      # Closes the python script
    
    #P1.update()
    #E1.move()
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    #DISPLAYSURF.fill(WHITE)
    #P1.draw(DISPLAYSURF)
    #E1.draw(DISPLAYSURF)
    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 
    #To be run if collision occurs between Player and any Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('./resources/crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()     

    pygame.display.update()     # After all computation is done, the display is updated. We can add more but becomes power intensive.
    FramePerSec.tick(FPS)   #Setting the frame rate of 60fps