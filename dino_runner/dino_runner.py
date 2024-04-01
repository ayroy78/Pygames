#GOOGLE CHROME DINO RUNNER

import pygame
import random
import time

pygame.mixer.init()

pygame.init()

screen_width = 900
screen_height = 400
ground = 300
birdy = 100
jumptune = pygame.mixer.Sound('jump.wav')
pygame.mixer.music.load('tune.mp3')

pygame.display.set_icon(pygame.image.load('cac2.bmp'))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Runner")


welcome_screen = pygame.transform.scale(pygame.image.load('welcome_screen.bmp'), (screen_width, screen_height)).convert_alpha()
lose_screen = pygame.transform.scale(pygame.image.load('lose_screen.bmp'), (screen_width, screen_height)).convert_alpha()

cac1 = pygame.transform.scale(pygame.image.load('cac1.bmp'), (40, 60)).convert_alpha()
cac2 = pygame.transform.scale(pygame.image.load('cac2.bmp'), (60, 60)).convert_alpha()
bird = pygame.transform.scale(pygame.image.load('bird.bmp'), (50, 30)).convert_alpha()

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

fps = 60
clock = pygame.time.Clock()

class player():
    def __init__(self, width, height, pic):
        self.width = width
        self.height = height
        self.pic = [pygame.transform.scale(pygame.image.load(pic[0]), (self.width, self.height)).convert_alpha(),pygame.transform.scale(pygame.image.load(pic[1]), (self.width, self.height)).convert_alpha(),pygame.transform.scale(pygame.image.load(pic[2]), (self.width, self.height)).convert_alpha(),pygame.transform.scale(pygame.image.load(pic[3]), (self.width, self.height)).convert_alpha()]
        self.x = screen_width/2
        self.y = ground - self.height
        self.jump = False
        self.jumpcount = 10
        self.walkcount = 1

    def move(self):
        if self.jump:
            if self.jumpcount ==10:
                pygame.mixer.Sound.play(jumptune)
                
            if self.jumpcount>0:
                self.y = self.y - ((self.jumpcount)**(2.0))*(0.5)
                self.jumpcount = self.jumpcount - 1
            elif -10<=self.jumpcount<=0:
                self.y = self.y + ((self.jumpcount)**(2.0))*(0.5)
                if self.y>ground - self.height:
                    self.y = ground - self.height
                self.jumpcount = self.jumpcount -1
            else:
                self.jump = False
                self.jumpcount = 10

    def draw(self):
        if self.walkcount<=3:
            screen.blit(self.pic[0], (self.x, self.y))
        elif 4<=self.walkcount<=6:
            screen.blit(self.pic[1], (self.x, self.y))
        elif 7<=self.walkcount<=9:
            screen.blit(self.pic[2], (self.x, self.y))
        else:
            screen.blit(self.pic[3], (self.x, self.y))

        self.walkcount = self.walkcount+1
        if self.walkcount==13:
            self.walkcount = 1


def generate_obstacles(time,obstaclelist):
    if time<=2500:
        if time%90==0:
            r =random.randint(1,9)
            if r<=4:
                obstaclelist.append([0,'cac1'])
            elif 4<r<=7:
                obstaclelist.append([0,'cac2'])
            else:
                obstaclelist.append([0,'bird'])
    elif 2500<time<=5000:
        if time%70==0:
            r =random.randint(1,9)
            if r<=4:
                obstaclelist.append([0,'cac1'])
            elif 4<r<=7:
                obstaclelist.append([0,'cac2'])
            else:
                obstaclelist.append([0,'bird'])
    elif 5000<time<=7500:
        if time%50==0:
            r =random.randint(1,9)
            if r<=4:
                obstaclelist.append([0,'cac1'])
            elif 4<r<=7:
                obstaclelist.append([0,'cac2'])
            else:
                obstaclelist.append([0,'bird'])
    else:
        if time%30==0:
            r =random.randint(1,9)
            if r<=4:
                obstaclelist.append([0,'cac1'])
            elif 4<r<=7:
                obstaclelist.append([0,'cac2'])
            else:
                obstaclelist.append([0,'bird'])
                

def move_obstalces(obstaclelist):
    for ob in obstaclelist:
        ob[0] = ob[0] - 10
        if ob[0]+ screen_width <=-100: #choosing a buffer, a certain distance left from screen after which obstacle is deleted
            obstaclelist.remove(ob)

def draw_obstacles(obstaclelist):
    for ob in obstaclelist:
        if ob[1]=='cac1':
            screen.blit(cac1, (ob[0]+screen_width,ground-cac1.get_height()))
        elif ob[1] == 'cac2':
            screen.blit(cac2, (ob[0]+screen_width,ground-cac2.get_height()))
        else:
            screen.blit(bird, (ob[0]+screen_width,birdy))

            
def check_collision(x,y, width, height, obstaclelist):
    global lose
    for ob in obstaclelist:
        if ob[1]=='cac1':
            if abs(ob[0]+screen_width+cac1.get_width()/2 - (x+width/2))<=cac1.get_width()/2.5 + width/2.5 and abs(ground-cac1.get_height()/2 - (y+height/2))<=cac1.get_height()/2.5 + height/2.5:
                lose =True
                time.sleep(1)
        elif ob[1]=='cac2':
            if abs(ob[0]+screen_width+cac2.get_width()/2 - (x+width/2))<=cac2.get_width()/2.5 + width/2.5 and abs(ground-cac2.get_height()/2 - (y+height/2))<=cac2.get_height()/2.5 + height/2.5:
                lose =True
                time.sleep(1)
        else:
            if abs(ob[0]+screen_width+bird.get_width()/2 - (x+width/2))<=bird.get_width()/2 + width/2 and abs(birdy-bird.get_height()/2 - (y+height/2))<=bird.get_height()/2 + height/2:
                lose =True
                time.sleep(1)

    
font=pygame.font.SysFont(None, 25)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

    
dino = player(80,80,['dino_1.png','dino_2.png','dino_3.png','dino_4.png'])

def start():
    pygame.mixer.music.play(-1)
    play = True
    while play:
        
        screen.blit(welcome_screen, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()

        pygame.display.update()
        clock.tick(fps)
    #REQUIRED so that pygame quits
    pygame.quit()
    quit()

    
def gameloop():
   
    play = True
    
    global lose
    lose = False
    
    dino.x = screen_width/2
    dino.y = ground - dino.height
    dino.jump = False
    dino.jumpcount = 10
    dino.walkcount = 0
    obstaclelist = []
    score = 0
    time = 0
    
    while play:   
        if lose:
            screen.blit(lose_screen, (0, 0))
            text_screen(str(score), red, 0.625*screen_width, screen_height*0.70)

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
           
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False

                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        dino.jump = True

            generate_obstacles(time, obstaclelist)
            move_obstalces(obstaclelist)
            dino.move()


            screen.fill(white)
            dino.draw()
            draw_obstacles(obstaclelist)
            
            pygame.draw.line(screen, black, (0,ground),(screen_width,ground))
            check_collision(dino.x,dino.y, dino.width, dino.height, obstaclelist)
            score = time
            text_screen('SCORE: '+ str(score), black, 750, 25)
            time = time +1
            
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

start()
                   
            
