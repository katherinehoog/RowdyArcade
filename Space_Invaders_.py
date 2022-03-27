#!/usr/bin/env python
# coding: utf-8

# # SPACE INVADERS

# In[2]:


#reference: https://www.geeksforgeeks.org/building-space-invaders-using-pygame-python/
#import statements
#source code from styles
import pygame
import random
import math
from pygame import mixer
import os


# # FUNCTIONS

# In[3]:


def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


# In[4]:


def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# In[5]:


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    restart_text = restart_font.render("Press R to restart", True, (255, 255, 255))
    return_to_menu_text = return_to_menu_font.render("Press M to return to menu", True, (255,255,255))
    
    screen.blit(game_over_text, (190, 250)) #text, and then the position
    screen.blit(restart_text, (185, 150)) #text, and then the position
    screen.blit(return_to_menu_text, (110, 50)) #text, and then the position
    
    #to restart or to return to a menu
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            running_game()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:
            menu()
    
    


# In[6]:


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


# In[7]:


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


# In[8]:


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


# # Setting Up the Game

# In[9]:


# initializing pygame
pygame.init()

#changing the working directory 
os.chdir('C:/Users/swapo/Documents/pygame') # change working directory


# In[10]:


# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# In[11]:


# caption and icon
pygame.display.set_caption("Welcome to Space\Invaders Game")


# In[12]:


# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)


# In[13]:


# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 50)
return_to_menu_font = pygame.font.Font('freesansbold.ttf', 50)


# In[14]:


# Background Sound
mixer.music.load('background.wav') #REPLACE
mixer.music.play(-1)


# In[15]:


# player
playerImage = pygame.image.load('spaceship.png') #REPLACE
player_X = 370
player_Y = 523
player_Xchange = 0
  


# In[16]:


# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
num_of_invaders = 8
  
for num in range(num_of_invaders):
    invaderImage.append(pygame.image.load('alien.png')) #REPLACE
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(0.5)
    invader_Ychange.append(50)
    


# In[17]:


# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('bullet.png') #REPLACE
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"
  


# # Controller

# In[18]:


# game loop
running = True
while running:
  
    # RGB
    #black background
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
  
        # Controling the player movement
        # from the arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -0.5
            if event.key == pygame.K_RIGHT:
                player_Xchange = 0.5
            if event.key == pygame.K_SPACE:
                
                # Fixing the change of direction of bullet
                if bullet_state == "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('bullet.wav') #REPLACE
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            player_Xchange = 0
  
    # adding the change in the player position
    player_X += player_Xchange
    for i in range(num_of_invaders):
        invader_X[i] += invader_Xchange[i]
  
    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange
  
    # movement of the invader
    for i in range(num_of_invaders):
        
        if invader_Y[i] >= 450:
            if abs(player_X-invader_X[i]) < 80:
                for j in range(num_of_invaders):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('explosion.wav') #REPLACE
                    explosion_sound.play()
                game_over()
                break
  
        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]
        
        # Collision
        collision = isCollision(bullet_X, invader_X[i],bullet_Y, invader_Y[i])
        if collision:
                score_val += 1
                bullet_Y = 600
                bullet_state = "rest"
                invader_X[i] = random.randint(64, 736)
                invader_Y[i] = random.randint(30, 200)
                invader_Xchange[i] *= -1
  
        invader(invader_X[i], invader_Y[i], i)
  
  
    # restricting the spaceship so that
    # it doesn't go out of screen
    if player_X <= 16:
            player_X = 16
    elif player_X >= 750:
            player_X = 750
  
  
    player(player_X, player_Y)  
    show_score(scoreX, scoreY)
    pygame.display.update()
    

