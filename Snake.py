#!/usr/bin/env python
# coding: utf-8

# # Snake

# In[1]:


# import statements
import pygame
import time
import random
import os


# In[2]:


# changes working directory
os.chdir('C:/Users/cecab/OneDrive/Documents/snake')


# In[3]:


# setting up colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (124,252,0)


# In[4]:


# initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# create sound object for sound effects
bite = pygame.mixer.Sound('bite.mp3')

# sets up the display
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake')

# makes the screen black
dis.fill(black)

# FPS (frames per second) controller
fps = pygame.time.Clock()


# In[5]:


# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]

# snake direction
direction = 'RIGHT'
change_to = direction

# speed of snake
snake_speed = 10

# fruit position
fruit_position = [random.randrange(1, (dis_width//10)) * 10,
                  random.randrange(1, (dis_height//10)) * 10]
fruit_spawn = True


# In[6]:


# initial score
score = 0


# # Function

# In[7]:


def display_score(color):
    
    # font object for the score
    score_font = pygame.font.Font('Pixeboy.ttf', 35)
    
    # display surface object for score
    score_surface = score_font.render('Score: ' + str(score), True, color )
    
    # make a rectangular object for the text surface object
    score_rect = score_surface.get_rect()
    
    # place the text on the window
    dis.blit(score_surface, score_rect)


# In[8]:


def game_over():
    
    # create font object
    my_font = pygame.font.SysFont('Pixeboy.ttf', 50)
    
    # display surface object for game over screen
    game_over_surface = my_font.render('Score : ' + str(score), True, white)
    
    # make a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()
    
    # position the text
    game_over_rect.midtop = (dis_width/2, dis_height/4)
    
    # place text on the window
    dis.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # quits the program after 5 seconds
    time.sleep(4)
    
    # closes pygame library
    pygame.quit()
    
    # ends the program
    quit()


# In[9]:


def eat():
    
    # eating sound
    bite.play()


# # Main

# In[10]:


while True:
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            elif event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
        
    # dealing with two key presses   
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
        
    # Snake body growing mechanism if fruits and snakes collide then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        eat()
        # increases score
        score += 10
        
        # increases speed
        snake_speed += 2
        
        # sets up condition for another fruit to spawn
        fruit_spawn = False
    else:
        snake_body.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (dis_width//10)) * 10,
                          random.randrange(1, (dis_height//10)) * 10]
         
    fruit_spawn = True
    
    dis.fill(black)
     
    for pos in snake_body:
        pygame.draw.rect(dis, green, pygame.Rect(
          pos[0], pos[1], 10, 10))
         
    pygame.draw.rect(dis, white, pygame.Rect(
      fruit_position[0], fruit_position[1], 10, 10))
 
    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > dis_width-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > dis_height-10:
        game_over()
     
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
     
    # displaying score countinuously
    display_score(white)
     
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)

