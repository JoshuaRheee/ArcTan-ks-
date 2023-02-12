'''
Steps Needed to run
1. Install Pip
2. Install pygame
3. Make sure all fonts and images downloaded in the same directory
'''

import pygame, sys
import time
import random
import tkinter as tk
import math

#Currently only accepts basic functions: x - x^4, sin(x),cos(x),tan(x)


pygame.init()

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

gameWin = pygame.display.set_mode((width, height))
pygame.display.set_caption('ARCTAN(KS)')
clock = pygame.time.Clock()


background = pygame.image.load("tank background.jpeg")
background = pygame.transform.scale(background, (width, height))


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


def controlsWin():
    button1 = Button("Play", (width*.33, height*.85),  font=30)

    button2 = Button("Main", (width*.48, height*.85), font=30)

    button3 = Button("Quit", (width*.63, height*.85), font=30)


    while True:
        '''gameWin.fill('#000000')''' #if we want background color black
        gameWin.blit(background,(0,0))
        Green = (0, 255, 0)
        show_message("ARCTAN(KS)", '#FF9526', -200, size="large")
        show_message("Instructions", '#EF4423', -100, size="medium")
        show_message("Enter  functions  to  determine  the  trajectory  of  your  missile", '#4FAF44', -30)
        show_message("Use  the  correct  function  to  avoid  the  obstacles", '#4FAF44', 30)
        show_message("and  obliterate  the  enemy  tank!", '#4FAF44', 90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event,'play')
            button2.click(event,'main')
            button3.click(event,'quit')
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
        '''gameWin.fill('#000000')''' #if we want home page background vintage yellow
        gameWin.blit(background,(0,0))
        Green = (0, 255, 0)
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
class level:
    def __init__(self,allyTank,enemyTank,increment,obstacles):
        self.allyTank = allyTank
        self.enemyTank = enemyTank
        self.increment = increment
        self.obstacles = obstacles


level1 = level([0,0],[3, 3],1,[])
level2 = level([-1,1],[2,1],1,[[0,10,1,9.5]])
level3 = level([-5,0],[5, -1],1,[5,10,1,9.5])
level4 = level([1.5,0],[4, 9],1,[0,10,1,9.5])
level5 = level([-6,3],[1, -3],1,[8,10,1,9.5])
level6 = level([-1,-4],[3, -3],1,[0,10,1,9.5])

def mainGame():
    count = 1
    root = tk.Tk()

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    BLACK = (0, 0, 0)
    GREEN = (0, 100, 0)
    BLUE = (65, 105, 225)

    height = height
    width = width

    def main():
        global SCREEN, CLOCK, font_color, font_obj, playerImg, enemyImg, blockSize
        pygame.init()
        SCREEN = pygame.display.set_mode((width, height))
        SCREEN.fill(BLACK)
        pygame.display.set_caption('ArcTan(ks)')

        font_color=(0,150,250)
        font_obj=pygame.font.Font("coure.fon",25)
        blockSize = round(float((height/20)))



        icon = pygame.image.load('tank.png')
        pygame.display.set_icon(icon)

        image_size = (40, 40)
        enemy_size = (50, 50)

        #Player
        playerImg = pygame.image.load("tank.png")
        playerImg = pygame.transform.scale(playerImg, image_size)

        #Enemy
        enemyImg = pygame.image.load("enemy.png")
        enemyImg= pygame.transform.scale(enemyImg, enemy_size)


        count = 1
        while True:
            fight(eval("level"+str(count)).allyTank,eval("level"+str(count)).enemyTank,eval("level"+str(count)).increment,eval("level"+str(count)).obstacles)
            count += 1
            pygame.display.update()

    def drawGrid(increment):
        for x in range(round(float(width*(7/16))), width, blockSize):
            for y in range(0, height, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, GREEN, rect, 1)


        count = 0
        for a in range(20+1):
            text_obj=font_obj.render(str(round(float((count-10)*increment),2)),True,font_color)
            SCREEN.blit(text_obj,(width*(7/16)+(count*blockSize-blockSize*3/8),height/2))
            count += 1

        count = 0
        for b in range(20+1):
            text_obj=font_obj.render(str(-(round(float((count-10)*increment),2))),True,font_color)
            SCREEN.blit(text_obj,(width*(11/16)+blockSize *3/4,(count*blockSize)))
            count += 1

    def fight(allyTank,enemyTank,increment,obstacles):

        #coordinates of character
        x = (width*(23/32))+(allyTank[0]*blockSize)-20
        y = (height/2)-(allyTank[1]*blockSize)-20

        original_ball_x = x + 20
        original_ball_y = y + 12

        ball_x = x + 20
        ball_y = y + 12
        #width and height of character
        vel = 2

        xval = 0
        x_dos = ball_x
        y_dos = ball_y

        y_cos = ball_y + 60

        tan_right_bound = x + 100;


        poly_x = 1
        poly_y = 200

        pygame.display.set_caption("Space Invade")

        enemyX = (width*(23/32))+(enemyTank[0]*blockSize)-25
        enemyY = (height/2)-(enemyTank[1]*blockSize) -25
        enemyX_change = 0

        base_font = pygame.font.Font(None, 32)
        user_text = ''

        input_rect = pygame.Rect(0,0,800, 32)
        color = pygame.Color('lightskyblue3')

        user_input = ""

        def player(x, y):
            SCREEN.blit(playerImg, (x,y))
        def enemy(x, y):
            SCREEN.blit(enemyImg, (x,y))


        def isCollision(enemyX, enemyY, ball_x, ball_y):
            distance = math.sqrt((math.pow(((enemyX)-ball_x),2)) + (math.pow(((enemyY+30)-ball_y), 2)))
            if distance < blockSize:
                return True
            else:
                return False


        run = True

        entered_input = False

        active = True

        while run:
            pygame.time.delay(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if active == True:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[0:-1]
                        elif event.key == pygame.K_RETURN:
                            active = False
                        else:
                            user_text += event.unicode

            collision = isCollision(enemyX, enemyY, ball_x, ball_y)

            if active == False:
                if user_text == "x":
                    ball_x = x_dos + xval* 50
                    xval += .1
                    ball_y = y_dos - xval * 50
                elif user_text == "x^2":
                    ball_x = x_dos + xval * 50
                    xval += .1
                    ball_y = y_dos - xval**2 * 50
                elif user_text == "x^3":
                    ball_x = x_dos + xval* 50
                    xval += .1
                    ball_y = y_dos - xval**3 * 50
                elif user_text == "x^4":
                    ball_x = x_dos + xval* 50
                    xval += .1
                    ball_y = y_dos - xval**4 * 50
                elif user_text == "sin(x)":
                    if (collision != True ):
                        ball_x = x_dos + xval* 50
                        xval += .1
                        ball_y = y_dos - (math.sin(xval) * 50)
                elif user_text == "cos(x)" and active == False:
                    if (collision != True):
                        ball_x = x_dos + xval* 50
                        xval += .1
                        ball_y = y_cos - (math.cos(xval) * 50)
                elif user_text == "tan(x)":
                    if (collision != True and (ball_x < tan_right_bound)):
                        ball_x = x_dos + xval* 50
                        xval += .1
                        ball_y = y_dos - (math.tan(xval) * 50)
                else:
                    active = True


            if (collision != True and (ball_y <=  0 or ball_x >= width)):
                count = 1
                SCREEN.fill((0,0,0))
                drawGrid(eval("level"+str(count)).increment)
                ball_x = original_ball_x
                ball_y = original_ball_y
                poly_x = 1

                xval = 0
                active = True
            elif (collision == True):
                break
                #fight(eval("level"+str(count)).allyTank,eval("level"+str(count)).enemyTank,eval("level"+str(count)).increment,eval("level"+str(count)).obstacles)
            elif active == True:
                count = 1
                SCREEN.fill((0,0,0))
                drawGrid(eval("level"+str(count)).increment)


            pygame.draw.rect(SCREEN, color, input_rect, 2)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            SCREEN.blit(text_surface, (input_rect.x,input_rect.y+5))

            pygame.draw.circle(SCREEN, (255, 0, 0), (ball_x, ball_y), 5)

            #for i in obstacles:
                #pygame.draw.rect(SCREEN, BLUE, pygame.Rect((width*(23/32)-i[2]*blockSize/2)+(i[0]*blockSize),(height/2)-(i[1]*blockSize),i[2]*blockSize,i[3]*blockSize),2,3)

            player(x, y)
            enemy(enemyX, enemyY)
            pygame.display.update()
    main()

mainWindow()
