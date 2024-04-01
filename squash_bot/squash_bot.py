#SQUASH BOT

import pygame
import random
import numpy as np

pygame.init()
pygame.mixer.init()

screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SQUASH BOT")

game_screen=pygame.transform.scale(pygame.image.load('game_screen.jpg'),(screen_width,screen_height)).convert_alpha()
lose_screen=pygame.transform.scale(pygame.image.load('lose_screen.jpg'),(screen_width,screen_height)).convert_alpha()
welcome_screen=pygame.transform.scale(pygame.image.load('welcome_screen.jpg'),(screen_width,screen_height)).convert_alpha()

fps = 60
clock = pygame.time.Clock()

class player():
    def __init__(self,height, width, pic):
        self.height=height
        self.width=width
        self.pic=pygame.transform.scale(pygame.image.load(pic),(self.width,self.height)).convert_alpha()
        self.x=screen_width/2
        self.y=screen_height-2*self.height
        self.velr=0
        self.vell=0
        self.velu=0
        self.veld=0

    def move_left(self):
        self.x=self.x-self.vell
        if self.x<0:
            self.x=0.0
            
    def move_right(self):
        self.x=self.x+self.velr
        if self.x>screen_width-self.width:
            self.x=screen_width-self.width

    def move_up(self):
        self.y=self.y-self.velu
        if self.y<screen_height/2:
            self.y=screen_height/2

    def move_down(self):
        self.y=self.y+self.veld
        if self.y>screen_height-self.height:
            self.y=screen_height-self.height


class ball():
    def __init__(self,colour, radius):
        self.colour=colour
        self.radius=radius
        self.x=random.randint(int(screen_width*(2/8)), int(screen_width*(6/8)))
        self.y=screen_height/2
        self.vel_x = 3
        self.vel_y = -3
        
    def move(self):
        self.x=self.x+self.vel_x
        self.y=self.y+self.vel_y
        
        if self.x<0:
            self.x = 0
            self.vel_x = -self.vel_x
            
        if self.x>screen_width-2*self.radius:
            self.x =screen_width-2*self.radius
            self.vel_x = -self.vel_x

        if self.y<self.radius:
            self.y = self.radius
            self.vel_y = -self.vel_y
        
def draw_player(screen,ob):
    screen.blit(ob.pic,(ob.x,ob.y))
    pygame.draw.rect(screen,(255,0,0),[ob.x,ob.y,ob.width,ob.height],1)

def draw_ball(screen,ob):
    pygame.draw.circle(screen, ob.colour, (ob.x, ob.y), ob.radius)


font=pygame.font.SysFont(None, 35)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

def start():
    pygame.mixer.music.load('tune.mp3')
    pygame.mixer.music.play(-1)
    
    play = True
    while play:
        
        screen.blit(welcome_screen, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        pygame.display.update()
        clock.tick(fps)
    #REQUIRED so that pygame quits
    pygame.quit()
    quit()


#balls and racquets are main objects of the game   
raq = player(50, 50, 'player2.png')
b1 = ball((255,0,0),10)
b2 = ball((0,255,0),10)

def main():
    pygame.mixer.music.load('tune.mp3')
    pygame.mixer.music.play(-1)

    #re-initialize everything for when the player loses and wants to try again
    raq.x=screen_width/2
    raq.y=screen_height-2*raq.height
    raq.velr=0
    raq.vell=0
    raq.velu=0
    raq.veld=0

    b1.x=random.randint(int(screen_width*(2/8)), int(screen_width*(6/8)))
    b1.y=screen_height/2
    b1.vel_x = 3
    b1.vel_y = -3

    b2.x=random.randint(int(screen_width*(2/8)), int(screen_width*(6/8)))
    b2.y=screen_height/2
    b2.vel_x = 3
    b2.vel_y = -3
    
    play = True
    lose = False
    score = 0
    while play:
        if lose:
            screen.blit(lose_screen, (0, 0))

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()
                
        else:
            #all user inputs
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False

                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RIGHT:
                        raq.velr = 5

                    if event.key == pygame.K_LEFT:
                        raq.vell = 5
                        
                    if event.key == pygame.K_DOWN:
                        raq.veld = 5

                    if event.key == pygame.K_UP:
                        raq.velu = 5
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        raq.velr = 0

                    if event.key == pygame.K_LEFT:
                        raq.vell = 0
                        
                    if event.key == pygame.K_DOWN:
                        raq.veld = 0

                    if event.key == pygame.K_UP:
                        raq.velu = 0
                    
           
            raq.move_right()
            raq.move_left()
            raq.move_up()
            raq.move_down()

            screen.blit(game_screen,(0,0))

            #increase speed as the score gets higher

            if 100<=score<=250:

                b1.vel_x = np.sign(b1.vel_x)*3.5
                b1.vel_y = np.sign(b1.vel_y)*3.5
                
            elif 250<=score<=500:
                b1.vel_x = np.sign(b1.vel_x)*4
                b1.vel_y = np.sign(b1.vel_y)*4

            else:
                b1.vel_x = np.sign(b1.vel_x)*3
                b1.vel_y = np.sign(b1.vel_y)*3
                

            
            #one ball only
            if score<=500:
                
                if ( 0<=(raq.x-b1.x)<= b1.radius or 0<=(b1.x-raq.x)<=raq.width+b1.radius) and abs(raq.y-b1.y)<= b1.radius:
                    score = score+50
                    b1.y = b1.y - 2*b1.radius  #make sure that the ball is immediately front of the player
                    b1.vel_y = -abs(b1.vel_y)  #make sure that the speed is negative and ball moves upwards
                    

                b1.move()
                draw_ball(screen, b1)

                if b1.y >= screen_height:
                    lose = True
                    pygame.mixer.music.load('lose.mp3')
                    pygame.mixer.music.play()
                
           
                
            #two balls
            elif score > 500:
                if ( 0<=(raq.x-b1.x)<= b1.radius or 0<=(b1.x-raq.x)<=raq.width+b1.radius) and abs(raq.y-b1.y)<= b1.radius:
                    score = score+50
                    b1.y = b1.y - 2*b1.radius  
                    b1.vel_y = -abs(b1.vel_y)  

                if ( 0<=(raq.x-b2.x)<= b2.radius or 0<=(b2.x-raq.x)<=raq.width+b2.radius) and abs(raq.y-b2.y)<= b2.radius:
                    score = score+50
                    b2.y = b2.y - 2*b2.radius  
                    b2.vel_y = -abs(b2.vel_y)  
   

                if abs(b1.x-b2.x)<=b1.radius + b2.radius and abs(b1.y-b2.y)<=b1.radius+b2.radius:
                    b1.vel_y = -b1.vel_y
                    b1.vel_x = -b1.vel_x

                    b2.vel_y = -b2.vel_y
                    b2.vel_x = -b2.vel_x
                    
                b1.move()
                b2.move()

                draw_ball(screen, b1)
                draw_ball(screen, b2)

                if b1.y >= screen_height or b2.y>= screen_height:
                    lose = True
                    pygame.mixer.music.load('lose.mp3')
                    pygame.mixer.music.play()
                
            draw_player(screen, raq)
            text_screen("Score: "+ str(score),(255,255,255),5,10)
        pygame.display.update()
        clock.tick(fps)
            
    pygame.quit()
    quit()

start()

