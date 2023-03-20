'''
Check the README file prior to running
'''

#Libraries
import pygame, sys
import time
import random
import tkinter as tk
import math
from sympy import var
from sympy import sympify

#Setting up basic variables and initilaizing the program
pygame.init()
root = tk.Tk()
clock = pygame.time.Clock()

#Getting the width and height in order to scale our game based on the dimensions of the user's screen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#Setting the dimensions of the game to the entirety of their screen (Fullscreen)
gameWin = pygame.display.set_mode((width, height))

#What the application name shows as in the top left corner or when hovered
pygame.display.set_caption('ARCTAN(KS)')


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

#Function that displays text
def show_message(msg, color, y_displace=0, size="small"):
    textSurf, textRect = textObjects(msg, color, size)
    textRect.center = (int(width / 2), int(height / 2) + y_displace)
    gameWin.blit(textSurf, textRect)


class Button:
#creats buttonns
    def __init__(self, text,pos, font, bg="#F6EB14"):
        self.x, self.y = pos
        self.font = pygame.font.Font("ARCADECLASSIC.TTF", font)
        self.text=text
        self.text = self.font.render(self.text, 1, pygame.Color("#F6EB14"))
        self.change_text(bg)

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
                        mainGame()

                    if action == "main":
                        mainWindow()


#Setting the placement of the buttons, which are placed based on the user's screen
def controlsWin():
    button1 = Button("Play", (width*.33, height*.85),  font=30)

    button2 = Button("Main", (width*.48, height*.85), font=30)

    button3 = Button("Quit", (width*.63, height*.85), font=30)


    while True:
        gameWin.blit(background,(0,0))
        Green = (0, 255, 0)

        #Instructions printed
        show_message("ARCTAN(KS)", '#FF9526', -200, size="large")
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

        #Displaying the buttons
        button1.show()
        button2.show()
        button3.show()

        clock.tick(30)
        pygame.display.update()




def mainWindow ():
    button1 = Button("Play", (width*.48,height*.65),  font=30)

    button2 = Button("Controls", (width*.46,height*.72), font=30)

    button3 = Button("Quit", (width*.48,height*.80), font=30)


    while True:
        gameWin.blit(background,(0,0))
        Green = (0, 255, 0)
        #More menu text
        show_message("ARCTAN(KS)", '#FF9526', -150, size="large")
        show_message("Welcome to the game!", '#A4FC52',-30, size="medium")
        show_message("Choose any of the following to move forward", '#A4FC52', 50, size="medium")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'controls')
            button3.click(event,'quit')
        button1.show()
        button2.show()
        button3.show()

        clock.tick(30)
        pygame.display.update()

#A basic class format is used to create levels, which takes in positions of tanks and obstacles
class level:
    def __init__(self,allyTank,enemyTank,increment,obstacles):
        self.allyTank = allyTank
        self.enemyTank = enemyTank
        self.increment = increment
        self.obstacles = obstacles

#All the levels set up
level1 = level([0,0],[3, 3],1,[])
level2 = level([-1,1],[2,1],1,[[0,10,1,9.5]])
level3 = level([-5,0],[5, -1],1,[5,10,1,9.5])
level4 = level([1.5,0],[4, 9],1,[0,10,1,9.5])
level5 = level([-6,3],[1, -3],1,[8,10,1,9.5])
level6 = level([-1,-4],[3, -3],1,[0,10,1,9.5])

def mainGame():
    count = 1

    #RGB values of these colors
    BLACK = (0, 0, 0)
    GREEN = (0, 100, 0)
    BLUE = (65, 105, 225)

    def main():
        #globalizing variables to be used in various functions
        global SCREEN, CLOCK, font_color, font_obj, playerImg, enemyImg, blockSize

        #Initializing basic variables
        pygame.init()
        SCREEN = pygame.display.set_mode((width, height))
        SCREEN.fill(BLACK)
        pygame.display.set_caption('ArcTan(ks)')

        #Font configuration
        font_color=(0,150,250)
        font_obj=pygame.font.Font("coure.fon",25)

        #The size of each block in the grid
        blockSize = round(float((height/20)))

        #Icon in top left corner of application
        icon = pygame.image.load('tank.png')
        pygame.display.set_icon(icon)

        #Size of the enemy and player
        image_size = (40, 40)
        enemy_size = (50, 50)

        #Player
        playerImg = pygame.image.load("tank.png")
        playerImg = pygame.transform.scale(playerImg, image_size)

        #Enemy
        enemyImg = pygame.image.load("enemy.png")
        enemyImg= pygame.transform.scale(enemyImg, enemy_size)


        levelCount = 1
        while True:
            fight(eval("level"+str(levelCount)).allyTank,eval("level"+str(levelCount)).enemyTank,eval("level"+str(levelCount)).increment,eval("level"+str(levelCount)).obstacles)
            levelCount += 1
            pygame.display.update()

    def drawGrid(increment):
        #drawing the grid by placing rectangles
        for x in range(round(float(width*(7/16))), width, blockSize):
            for y in range(0, height, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, GREEN, rect, 1)

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
    def fight(allyTank,enemyTank,increment,obstacles):
        x = var('x')

        #coordinates of character
        charx = (width*(23/32))+(allyTank[0]*blockSize)-20
        chary = (height/2)-(allyTank[1]*blockSize)-20

        #Enemy Coordinates
        enemyX = (width*(23/32))+(enemyTank[0]*blockSize)-25
        enemyY = (height/2)-(enemyTank[1]*blockSize) -25

        def player(x, y):
            SCREEN.blit(playerImg, (x,y))
        def enemy(x, y):
            SCREEN.blit(enemyImg, (x,y))

        #coordinates of where the ball starts
        original_ball_x = charx + 20
        original_ball_y = chary + 12

        #coordinates of the ball
        ball_x = charx + 20
        ball_y = chary + 12

        #width and height of character
        xval = 0
        x_dos = ball_x
        y_dos = ball_y

        #What the application name is displayed as at the top left
        pygame.display.set_caption("Space Brawl")

        #User input configuration
        base_font = pygame.font.Font(None, 32)
        user_text = ''
        input_rect = pygame.Rect(0,0,800, 32)
        color = pygame.Color('lightskyblue3')

        #Checks if the projectile collides with the enemy
        def isCollision(enemyX, enemyY, ball_x, ball_y):
            distance = math.sqrt((math.pow(((enemyX)-ball_x),2)) + (math.pow(((enemyY+30)-ball_y), 2)))
            if distance < blockSize/2:
                return True
            else:
                return False

        #Loop for program to run
        run = True
        typing = True
        while run:
            pygame.time.delay(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
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
                
            #Check if it collides with walls or enemy
            collision = isCollision(enemyX, enemyY, ball_x, ball_y)
            #If the ball collides with the wall, restart the level
            if (collision != True and (ball_y <=  0 or ball_x >= width)):
                count = 1
                SCREEN.fill((0,0,0))
                drawGrid(eval("level"+str(count)).increment)
                ball_x = original_ball_x
                ball_y = original_ball_y
                xval = 0
                typing = True
            #If ball collides, break out of the level
            elif (collision == True):
                break
            elif typing == True:
                count = 1
                SCREEN.fill((0,0,0))
                drawGrid(eval("level"+str(count)).increment)

            #Printing the ball and user input text box
            pygame.draw.rect(SCREEN, color, input_rect, 2)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            SCREEN.blit(text_surface, (input_rect.x,input_rect.y+5))
            pygame.draw.circle(SCREEN, (255, 0, 0), (ball_x, ball_y), 5)

            #for i in obstacles:
                #pygame.draw.rect(SCREEN, BLUE, pygame.Rect((width*(23/32)-i[2]*blockSize/2)+(i[0]*blockSize),(height/2)-(i[1]*blockSize),i[2]*blockSize,i[3]*blockSize),2,3)

            #Print the player and enemy
            player(charx, chary)
            enemy(enemyX, enemyY)

            #Displaying everything
            pygame.display.update()

    #The main function is called to run all these functions
    main()

#Main window is the first thing that is run, which will call all other functions, which are nested within each other
mainWindow()
