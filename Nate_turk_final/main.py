# This file was created by Nate Turkington

#Sources: 
# help + basecode from https://www.youtube.com/watch?v=y2UzjhnJN_k&list=PLhTjy8cBISEo3SzET7Fc3-b4miKWp41yX&index=13 
# content from kids can code: http://kidscancode.org/blog/
# help from geeks for geeks: https://www.geeksforgeeks.org/
# help from https://www.youtube.com/watch?v=gnlWy-qi6Rs&list=PLhTjy8cBISEo3SzET7Fc3-b4miKWp41yX&index=4
# help from https://www.youtube.com/@buildwithpython "tutorial"

#Goals:
# Movement from left to right for the player
# Create lasers that come out of the players space ship to hit the enemies
# Movement from enemies to go to the side to the boundary and as they hit go down and to the other side boundary


# Import libraries 
# os allows access to the image files 
# pygame is the main library which controls the game loop and other functions 
# random spanws in the enemies in random places 
# math is how i wrote the collisions using the distance between 2 mid points equation 
import os
import pygame
import random
import math
# initialize pygame 
pygame.init ()
 
# set up the screen using pygame
screen = pygame.display.set_mode ((800,600))
 
# set up the images and name of the game window
pygame.display.set_caption ("Space Raiders")
icon = pygame.image.load ('space-ship.png')
pygame.display.set_icon(icon)
 
# Background
background = pygame.image.load ('screen.png')
 
# player (creates the space ship)
playerImg = pygame.image.load ('player.png')
playerX = 370
playerY = 480
playerX_change = 0
 
 
# Enemy (creates the enemy)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
 
# random enemy generation and controls score 
for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load ('enemy.png'))
    enemyX.append(random.randint (0,735))
    enemyY.append(random.randint (50,150))
    enemyX_change.append(2.5)
    enemyY_change.append(40)
 
# ready means you can't see the laser on the screen
# fire = the laser is currently moving 
# laser (creates the lazer)
# creates the image of the lazer by loading it from the other files within the folder 
laserImg = pygame.image.load ('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 7
laser_state = "ready"
 
# score
# font(what font the words appear in)
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
# size of the text
textX = 10 
textY = 10
 
#game over text 
over_font = pygame.font.Font('freesansbold.ttf',64)
# the function that shows the score on the screen and the screen.blit is what draws it 
def show_score (x,y):
    score = font.render("Score :" + str(score_value) , True, (255,255,255))
    screen.blit (score, ( x, y ))
# the function that shows the game over text when the game ends 
def game_over_text():
    over_text = font.render ("GAME OVER", True, (255,255,255))
    screen.blit (over_text, ( 200, 250))
# draws player
def player (x,y):
    screen.blit (playerImg, ( x, y ))
# draws enemy 
def enemy (x,y,i):
    screen.blit (enemyImg[i], ( x, y ))
# this is how the laser fires with the 2 states of the laser 
def fire_laser (x,y) :
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x+16,y+10))
# the library math allows the collision between the laser and emeny to run as using the distance between 2 mid points equation 
# the function gives us 4 cordinates to of where the enemies are and 2 where the lasers are
# using the math.sqrt it finds the square root of the whole equation
# then using math.pow we square the 2 values of enemy x - laser y and enemy y - laser y 
# if the distance between the laser and enemy is less then 27 pixels it is a colliosn 
def isCollision (enemyX,enemyY,laserX,laserY) :
    distance = math.sqrt ((math.pow(enemyX - laserX,2)) +  (math.pow(enemyY - laserY,2)))
    if distance <27:
        return True
    else:
        return False
# game loop
running = True 
while running: 
     # RGB
    screen.fill ((0,0,0))
    # background image
    screen.blit(background, (0,0))
 
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False
 
        # if key pressed check whether its right of left using the pygame librabry to detect the keys being pressed by the user 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_a :
               playerX_change = -3
            if event.key == pygame.K_d :
                 playerX_change = 3
            if event.key == pygame.K_SPACE :
                if laser_state is "ready":
                    laserX = playerX
                    fire_laser(laserX,laserY)
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a or event.key == pygame.K_d :
                playerX_change = 0
 
                
    # checking for boundaries and does not allow the player outside 
    playerX += playerX_change   
 
    if playerX <=0 :
        playerX = 0
    elif playerX >=736 :
        playerX = 736
 
    # laser movement (when the player pushes space the laser state changes and the code below allows for it to move as it is fired)
    if laserY <=0:
        laserY = 480
        laser_state == "ready"
    if laser_state == "fire":
        fire_laser(laserX,laserY)
        laserY -= laserY_change

 
    # enemy movement
    for i in range (num_of_enemies):
        # game over 
        if enemyY[i] > 440: 
            for j in range (num_of_enemies):
                enemyY [j] = 2000
            game_over_text ()
            break
        # this is how the enemies move when they hit the side boundaries they go down and move side to side
        enemyX[i] += enemyX_change[i]   
        if enemyX[i] <=0 :
                enemyX_change[i] = 2.5
                enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >=736 :
                enemyX_change[i] = -2.5
                enemyY[i] += enemyY_change[i]
    #collision between the lasers and the random enemies spawned in also controls how the score works 
        collision = isCollision (enemyX[i], enemyY[i], laserX,laserY)
        if collision: 
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint (0,735)
            enemyY[i] = random.randint (50,150)
 
        enemy( enemyX[i], enemyY[i], i)
 
# updates location of player and the score of the game 
    player( playerX, playerY)
    show_score (textX, textY)
    pygame.display.update()