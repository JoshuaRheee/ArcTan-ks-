'''
Check the README file prior to running
'''

#Libraries
import pygame, sys
import time
import random
import tkinter as tk
import math
from pygame.locals import *
from sympy import var
from sympy import sympify

#Setting up basic variables and initilaizing the program
pygame.init()
root = tk.Tk()
clock = pygame.time.Clock()

#RGB values of these colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
DARKGREEN = (0, 100, 0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (65, 105, 225)


#Getting the width and height in order to scale our game based on the dimensions of the user's screen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#Setting the dimensions of the game to the entirety of their screen (Fullscreen)
gameWin = pygame.display.set_mode((width, height))

#What the application name shows as in the top left corner or when hovered
pygame.display.set_caption('ARCTAN(KS)')

#Global Variables
SCREEN = pygame.display.set_mode((width, height))
blockSize = round(float((height/20)))

#Font configuration
font_color=(0,150,250)
font_obj=pygame.font.Font("coure.fon",25)

#Size of the enemy and player
image_size = (40, 40)
enemy_size = (50, 50)
#Player
playerImg = pygame.image.load("tank.png")
playerImg = pygame.transform.scale(playerImg, image_size)

#Enemy
enemyImg = pygame.image.load("enemy.png")
enemyImg= pygame.transform.scale(enemyImg, enemy_size)

#Using a jpeg as the background image
background = pygame.image.load("tankBackground.jpeg")
background = pygame.transform.scale(background, (width, height))

#Configuring fonts
def textObjects(text, color, size="small"):
    if size == "vsmall":
        font=pygame.font.SysFont("Courier", 15)
        textSurf = font.render(text, True, color)
    if size == "small":
        font=pygame.font.Font("ARCADECLASSIC.TTF", 35)
        textSurf = font.render(text, True, color)
    if size == "medium":
        font=pygame.font.Font("ARCADECLASSIC.TTF", 45)
        textSurf = font.render(text, True, color)
    if size == "large":
        font=pygame.font.Font("ARCADE.TTF", 150)
        textSurf = font.render(text, True, color)
    return textSurf, textSurf.get_rect()

#Function that displays menu text
def show_message(msg, color, y_displace=0, size="small"):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center = (int(width / 2), int(height / 2) + y_displace)
    gameWin.blit(textSurf, textRect)

def displayMessage(msg,ypos,color) :
    if (len(msg) > 44):
        letters = len(msg)
        lastVal = 0
        line = 0
        mostRecentSpace = 0
        for i in range(len(msg)):
            if (msg[i] == ' '):
                mostRecentSpace = i
            if (i % 44 == 0 or i == len(msg)-1):
                temp = msg[lastVal:mostRecentSpace]
                textSurf, textRect = textObjects(temp, (color), "small")
                textRect.center = (int(width*7/32), int((height / 2) + ypos + line * 60))
                gameWin.blit(textSurf, textRect)
                lastVal = mostRecentSpace
                i = mostRecentSpace
                line += 1
    else:
        textSurf, textRect = textObjects(msg, (color), "small")
        textRect.center = (int(width*7/32), int((height / 2) + ypos))
        gameWin.blit(textSurf, textRect)

    

#Detects the user's pointer location and returns whether it is in the rectangle or not
def pointInRectanlge(px, py, rw, rh, rx, ry):
        if px > rx and px < rx  + rw:
            if py > ry and py < ry + rh:
                return True
        return False

#A basic class format is used to create levels, which takes in positions of tanks and obstacles
class level:
    def __init__(self,allyTank,enemyTank,increment,obstacles,message):
        self.allyTank = allyTank
        self.enemyTank = enemyTank
        self.increment = increment
        self.obstacles = obstacles
        self.message = message

#All the levels set up
#level = level(allycoord,enemycoord,mapscaling,barrier,message)
level1 = level([0,0],[3, 3],1,[0,0,0,0],"this  game  will heavily  rely  on  your  knowledge  of  how  functions  are graphed! press  x  and  enter  to  continue")
level2 = level([0,0],[1,5],1,[0,0,0,0],"hmmm  how  do  you  hit  this  one")
level3 = level([-5,1],[0,0],1,[0,0,0,0],"try  this  one  on  for  size")
level4 = level([0,0],[3,8],1,[0.5,4,1,2],"try  to  avoid  the  red  obstacles  and  hit  your  target!  (this  one  needs  a  simple  quadratic  equation)")
level5 = level([-3,8],[0,0],1,[-2,4,1,2],"how  about  a  little  role  reversal")
level6 = level([-1,-8],[1,8],1,[-1,1,2,1],"lets  put  more  power  on  these")
level7 = level([-4,-8],[2,1],1,[-2,-2,1,4],"this  one  is  going  to  be  a  big  tight  think  about  how  you  can  expand  a  function  lengthwise")
level8 = level([-5,-5],[8,-3.5],1,[0,-4,1,1],"the  name  of  the  game  did  you  know  that  this  function's  y  value  approaches  but  never  touches  pi/2  as  it  goes  to  infinity")



number_of_levels = 8

class Button:

    def __init__(self, text,pos, font, bg="#F6EB14"):
        self.x, self.y = pos
        self.font = pygame.font.Font("ARCADECLASSIC.TTF", font)
        self.text=text
        self.text = self.font.render(self.text, 1, pygame.Color("#F6EB14"))
        self.change_text(bg)

    #Button class functions
    def change_text(self, bg="blue"):
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
    def show(self):
        gameWin.blit(self.text , (self.x, self.y))

    #Navigates the user to different menu's if button is clicked
    def click(self, event,action):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if action == "quit":
                        pygame.quit()
                        quit()

                    if action == "controls":
                        controlsWin()

                    if action == "play":
                        playGame()

                    if action == "main":
                        mainWindow()

                    if action == 'levels':
                        levelsMenu()
                    
                    if action == 'controls':
                        controlsWin()

    #Detects if the level is clicked
    def levelClicked(self,events):
        mousePos = pygame.mouse.get_pos()
        if pointInRectanlge(mousePos[0], mousePos[1], self.text.get_size()[0], self.text.get_size()[1], self.x, self.y):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False

#Levels Menu
def levelsMenu():

    #Creating all the buttons for the levels
    buttons = [Button(f"Level {i+1}", ((width/5 * (i%5) + width/14), 250 + (i * 20)),font = 30) for i in range(number_of_levels)]

    #Creating other buttons to navigate to different menus
    button1 = Button("Play", (width*.25, height*.85),  font=30)

    button2 = Button("Main", (width*.4, height*.85), font=30)

    button3 = Button("Quit", (width*.55, height*.85), font=30)

    button4 = Button("Controls", (width*.7, height*.85), font=30)

    while True:
        gameWin.blit(background,(0,0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        
        show_message("ARCTAN(KS)", '#FF9526', -400, size="large")
        show_message("Levels", '#EF4423', -320, size="medium")
        for button in buttons:
            #Displaying the buttons
            button.show()
            #Checking if clicked
            if button.levelClicked(events):
                levelDetected = 0
                levelDetected += round((button.x - width/14) / (width/5)) + 1
                levelDetected += 5 * math.floor(((button.y - 250) / 100))
                levelCount = 0
                while True:
                    if ((int(levelDetected) + (levelCount)) > number_of_levels) :
                        print(levelDetected)
                        print(levelCount)
                        victoryMenu()
                    fight(eval("level"+str(levelDetected+levelCount)).allyTank,eval("level"+str(levelDetected+levelCount)).enemyTank,eval("level"+str(levelDetected+levelCount)).increment,eval("level"+str(levelDetected+levelCount)).obstacles,eval("level"+str(levelDetected+levelCount)).message,(levelDetected+levelCount))
                    levelCount += 1

        #Displaying the menu buttons beneath
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'main')
            button3.click(event,'quit')
            button4.click(event,'controls')
        button1.show()
        button2.show()
        button3.show()
        button4.show()
        pygame.display.update()

#Controls window
def controlsWin():
    #Creating buttons to navigate to different menus
    button1 = Button("Play", (width*.25, height*.85),  font=30)

    button2 = Button("Main", (width*.4, height*.85), font=30)

    button3 = Button("Quit", (width*.55, height*.85), font=30)

    button4 = Button("Levels", (width*.7, height*.85), font=30)


    while True:
        gameWin.blit(background,(0,0))

        #Instructions text
        show_message("ARCTAN(KS)", '#FF9526', -400, size="large")
        show_message("Instructions", '#EF4423', -100, size="medium")
        show_message("Enter  functions  to  determine  the  trajectory  of  your  missile", '#4FAF44', -30)
        show_message("Use  the  correct  function  to  avoid  the  obstacles", '#4FAF44', 30)
        show_message("and  obliterate  the  enemy  tank!", '#4FAF44', 90)

        #Checks if button is clicked. If button is clicked it navigates to the corresponding page
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'main')
            button3.click(event,'quit')
            button4.click(event,'levels')

        #Displaying the buttons
        button1.show()
        button2.show()
        button3.show()
        button4.show()

        clock.tick(30)
        pygame.display.update()

#Main Menu
def mainWindow():
    button1 = Button("Play", (width*.48,height*.6),  font=30)

    button2 = Button("Controls", (width*.46,height*.74), font=30)

    button3 = Button("Quit", (width*.48,height*.81), font=30)

    button4 = Button("Levels", (width*.47,height*.67), font=30)


    while True:
        gameWin.blit(background,(0,0))
        #Main menu text
        show_message("ARCTAN(KS)", '#FF9526', -180, size="large")
        show_message("Welcome to the game!", '#A4FC52',-70, size="medium")
        show_message("Choose any of the following to move forward", '#A4FC52', 50, size="medium")

        #Checks if button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'controls')
            button3.click(event,'quit')
            button4.click(event,'levels')
        
        #Displaying the buttons
        button1.show()
        button2.show()
        button3.show()
        button4.show()

        clock.tick(30)
        pygame.display.update()

def victoryMenu():
    gameWin.blit(background,(0,0))
    #Victory
    
    #Creating buttons to navigate to different menus
    button1 = Button("Play", (width*.25, height*.85),  font=30)

    button2 = Button("Main", (width*.4, height*.85), font=30)

    button3 = Button("Quit", (width*.55, height*.85), font=30)

    button4 = Button("Levels", (width*.7, height*.85), font=30)


    while True:
        gameWin.blit(background,(0,0))

        #Instructions text
        show_message("ARCTAN(KS)", '#FF9526', -400, size="large")
        show_message("Congratulations!!!", '#EF4423', -200, size="large")
        show_message("You have officially beaten the game!!!", '#4FAF44', -120, size="medium")
        show_message("Thank you for playing!", '#4FAF44', -50, size="medium")
        show_message("This game was created by Joshua Rhee Ernest Wong and Thomas Kim at OwlHacks 2023", '#4FAF44', 20, size="medium")
        show_message("To the sponsors and staff that made this possible", '#4FAF44', 90, size="medium")
        show_message("Thank you so much! We hope to see you again next year!!!", '#4FAF44', 180, size="medium")

        #Checks if button is clicked. If button is clicked it navigates to the corresponding page
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'main')
            button3.click(event,'quit')
            button4.click(event,'levels')

        #Displaying the buttons
        button1.show()
        button2.show()
        button3.show()
        button4.show()

        clock.tick(30)
        pygame.display.update()

def playGame():
    count = 1

    #globalizing variables to be used in various functions
    global CLOCK

    #Initializing basic variables
    pygame.init()
    SCREEN.fill(BLACK)
    pygame.display.set_caption('ArcTan(ks)')

    #Icon in top left corner of application
    icon = pygame.image.load('tank.png')
    pygame.display.set_icon(icon)

    levelCount = 1
    while True:
        if levelCount > number_of_levels :
            victoryMenu()
        else :
            fight(eval("level"+str(levelCount)).allyTank,eval("level"+str(levelCount)).enemyTank,eval("level"+str(levelCount)).increment,eval("level"+str(levelCount)).obstacles,eval("level"+str(levelCount)).message,levelCount)
            levelCount += 1
        pygame.display.update()

def drawGrid(increment):
    #drawing the grid by placing rectangles
    for x in range(round(float(width*(7/16))), width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, DARKGREEN, rect, 1)

    #placing the x coord numbers
    count = 0
    for a in range(20+1):
        if (count != 10) :
            text_obj=font_obj.render(str(round(float((count-10)*increment),2)),True,font_color)
            SCREEN.blit(text_obj,(width*(7/16)+(count*blockSize-blockSize*3/8),height/2))
            count += 1
        else:
            count += 1
        
    #placing the y coord numbers
    count = 0
    for b in range(20+1):
        if (count != 10):
            text_obj=font_obj.render(str(-(round(float((count-10)*increment),2))),True,font_color)
            SCREEN.blit(text_obj,(width*(11/16)+blockSize *3/4,(count*blockSize)))
            count += 1
        else:
            count += 1
        
#The levels begin to play here
def fight(allyTank,enemyTank,increment,obstacles,message,levelNumber):

    mainButton = Button("Main", (10 + width * .08, height*.95), font=30)
    levelsButton = Button("Levels", (10 + width * .18, height*.95), font=30)
    controlsButton = Button("Controls", (10 + width * .28, height*.95), font=30)

    x = var('x')

    #Ally Coordinates
    charx = (width*(23/32))+(allyTank[0]*blockSize)-20
    chary = (height/2)-(allyTank[1]*blockSize)-20

    #Enemy Coordinates
    enemyX = (width*(23/32))+(enemyTank[0]*blockSize)-25
    enemyY = (height/2)-(enemyTank[1]*blockSize) -25

    #Obstacle
    obstacle = Rect((width*(23/32)-obstacles[2]*blockSize/2)+(obstacles[0]*blockSize),(height/2)-(obstacles[1]*blockSize),obstacles[2]*blockSize,obstacles[3]*blockSize)

    #coordinates of where the ball starts
    original_ball_x = charx + 20
    original_ball_y = chary + 20

    #coordinates of the ball
    ball_x = charx + 20
    ball_y = chary + 20

    #updating the position of the ball
    xval = 0
    x_dos = ball_x
    y_dos = ball_y
    
    def player(x, y):
        SCREEN.blit(playerImg, (x,y))
    def enemy(x, y):
        SCREEN.blit(enemyImg, (x,y))

    #What the application name is displayed as at the top left
    pygame.display.set_caption("Space Brawl")

    #User input configuration
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(0,0,800, 32)
    color = pygame.Color('lightskyblue3')

    #Checks if the projectile collides with the enemy
    def isCollision(enemyX, enemyY, ball_x, ball_y, ball, obstacle):
        distance = math.sqrt((math.pow((enemyX+25-ball_x),2)) + (math.pow((enemyY+25-ball_y), 2)))
        if distance < blockSize/2:
            return True
        else:
            return False
    

    #Loop for program to run
    run = True
    typing = True
    while run:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Check if buttons are clicked
            mainButton.click(event,'main')
            controlsButton.click(event,'controls')
            levelsButton.click(event,'levels')

            #Get user input. Configure backspace and return
            if typing == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                    elif event.key == pygame.K_RETURN:
                        typing = False
                    else:
                        user_text += event.unicode
        
        #When user is finished typing, compute what occurs with the function
        if typing == False:
            if user_text == "arctan(x)":
                ball_x = x_dos + xval* 50
                xval += .1
                ball_y = y_dos - (math.atan(xval) * 50)
            elif user_text == "log(x)":
                ball_x = x_dos + xval* 50
                xval += .1
                ball_y = y_dos - (math.log(xval) * 50 + 100)
            else: 
                function = sympify(user_text)
                ball_x = x_dos + xval * 50
                xval += .1
                ball_y = y_dos - float(function.subs(x,xval)) * 50
            
        #Check if it collides with the enemy
        #Ball
        ball = Rect(ball_x, ball_y, 5,5)
        collision = isCollision(enemyX, enemyY, ball_x, ball_y, ball, obstacle)

        #If the ball collides with the wall, restart the level
        if ((collision != True and (ball_y <=  0 or ball_y >= height or ball_x >= width)) or pygame.Rect.colliderect(ball,obstacle)):
            count = 1
            SCREEN.fill((BLACK))
            drawGrid(eval("level"+str(count)).increment)
            ball_x = original_ball_x
            ball_y = original_ball_y
            xval = 0
            typing = True
            user_text = ''

        #If ball collides with the enemy, break out of the level
        elif (collision == True):
            break
        elif typing == True:
            count = 1
            SCREEN.fill((BLACK))
            drawGrid(eval("level"+str(count)).increment)

        #Printing the ball and user input text box
        pygame.draw.rect(SCREEN, color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        SCREEN.blit(text_surface, (input_rect.x,input_rect.y+5))
        pygame.draw.circle(SCREEN, (255, 0, 0),(ball_x, ball_y), 5)

        #Create rectangles
        #rect(x coord, y coord, width, height)
        pygame.draw.rect(SCREEN, RED, obstacle,2,3)

        #Print the player and enemy
        player(charx, chary)
        enemy(enemyX, enemyY)

        #Displaying everything
        displayMessage("Level  " + str(levelNumber),-400,RED)
        displayMessage(message,-350,BLUE)
        displayMessage("TIPS",105,YELLOW)
        displayMessage("make  sure  you  do  not  directly  place  x  next  to  a  value  always  use  the  star  symbol  and  note  that  parenthesis  are  required  for  trigonometric  functions!  ",100, WHITE)

        mainButton.show()
        levelsButton.show()
        controlsButton.show()
        pygame.display.update()

#Main window is the first thing that is run, which will call all other functions, which are nested within each other
mainWindow()
