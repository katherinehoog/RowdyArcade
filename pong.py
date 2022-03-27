#!/usr/bin/env python
# coding: utf-8

# In[8]:


# imports and intializes pygame
import pygame
pygame.init()

# import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# displays screens and caption
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# defines colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# defines paddle and ball size
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 8

# defines font and winning score
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

# defines the paddle class 
class Paddle:
    COLOR = WHITE
    VEL = 4

    # creates the paddle size and location 
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # draws the paddles
    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    # moves the paddle up or down
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    # resets the paddles 
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# defines the ball class
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    #creates ball size and location
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    # draws ball
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    # allows movement
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # resets ball after point is won
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

# draws scorces 
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    # writes scores to screen 
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

# handles collison for ball and paddles
def collision(ball, paddleA, paddleB):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= paddleA.y and ball.y <= paddleA.y + paddleA.height:
            if ball.x - ball.radius <= paddleA.x + paddleA.width:
                ball.x_vel *= -1

                middle_y = paddleA.y + paddleA.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (paddleA.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= paddleB.y and ball.y <= paddleB.y + paddleB.height:
            if ball.x + ball.radius >= paddleB.x:
                ball.x_vel *= -1

                middle_y = paddleB.y + paddleB.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (paddleB.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# handles paddle movement with keys 
def paddle_movement(keys, paddleA, paddleB):
    if keys[pygame.K_w] and paddleA.y - paddleA.VEL >= 0:
        paddleA.move(up=True)
    if keys[pygame.K_s] and paddleA.y + paddleA.VEL + paddleA.height <= HEIGHT:
        paddleA.move(up=False)

    if keys[pygame.K_UP] and paddleB.y - paddleB.VEL >= 0:
        paddleB.move(up=True)
    if keys[pygame.K_DOWN] and paddleB.y + paddleB.VEL + paddleB.height <= HEIGHT:
        paddleB.move(up=False)

# is the main driver of the game
def main():
    run = True
    clock = pygame.time.Clock()

    paddleA = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddleB = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    # main event loop
    while run:
        clock.tick(60)
        draw(WIN, [paddleA, paddleB], ball, left_score, right_score)         
                
        # checks if escape key is pressed or if window is closed 
        for event in pygame.event.get():               
            if event.type == KEYDOWN:            
                if event.key == K_ESCAPE:        
                    run = False
            elif event.type == QUIT:             
                run = False 
                
                

        keys = pygame.key.get_pressed()
        paddle_movement(keys, paddleA, paddleB)

        ball.move()
        collision(ball, paddleA, paddleB)

        # adds to score at end of round
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # checks to see if player has won
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Winner Player 1!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Winner Player 2!"

        # if won display end screen 
        if won:
            WIN.fill(BLACK)
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(10000)
            ball.reset()
            paddleA.reset()
            paddleB.reset()
            left_score = 0
            right_score = 0
            
    pygame.quit()


if __name__ == '__main__':
    main()

# used to help create pong:
# https://realpython.com/pygame-a-primer/#conclusion
# https://www.101computing.net/pong-tutorial-using-pygame-adding-a-scoring-system/
# https://www.youtube.com/watch?v=Qf3-aDXG8q4
# In[ ]:




