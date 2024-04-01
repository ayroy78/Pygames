#SPACE INVADERS

import pygame
import random


pygame.init()
pygame.mixer.init()

screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) #let the default stay as a black window
pygame.display.set_caption("SPACE INVADERS")
fps = 60
clock = pygame.time.Clock()

heart = pygame.transform.scale(pygame.image.load('heart.bmp'),(20,20)).convert_alpha()
lose_screen = pygame.transform.scale(pygame.image.load('lose_screen.bmp'),(screen_width,screen_height)).convert_alpha()
home_screen = pygame.transform.scale(pygame.image.load('home_screen.bmp'),(screen_width,screen_height)).convert_alpha()
game_clear_screen = pygame.transform.scale(pygame.image.load('game_clear_screen.bmp'),(screen_width,screen_height)).convert_alpha()

class player():
    def __init__(self, width, height, pic):
        self.width = width
        self.height = height
        self.pic = pygame.transform.scale(pygame.image.load(pic),(self.width,self.height)).convert_alpha()
        self.x = screen_width/2
        self.y = 525
        self.vel = 0

    def move(self):
        self.x = self.x + self.vel
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def draw(self, screen):
        screen.blit(self.pic,(self.x,self.y))


class alien_squad():
    def __init__(self, width, height, pic):
        #individual properties
        self.width = width
        self.height = height
        self.pic = pygame.transform.scale(pygame.image.load(pic),(self.width,self.height)).convert_alpha()

        #group properties
        self.rectwidth = self.width*10
        self.rectheight = self.height*5
        self.rectx = 150
        self.recty = 50
        self.velx = -2
        self.vely = 30
        self.ls = []
        self.ymax = self.recty + self.rectheight  #initial maximum y-position
        
    def initialpositioning(self):
        y_pos = self.recty
        for i in range(0,5):
            x_pos = self.rectx
            for k in range(0,10):
                self.ls.append([x_pos, y_pos])
                x_pos = x_pos + self.width
            y_pos = y_pos + self.height
        
    def move(self):
        self.rectx = self.rectx + self.velx   
        for coordinate in self.ls:
            coordinate[0] = coordinate[0] + self.velx
            if self.rectx <=0 or self.rectx>= screen_width - self.rectwidth:
                coordinate[0] = coordinate[0] - self.velx
                coordinate[1] = coordinate[1] + self.vely
                
        if self.rectx <=0 or self.rectx>= screen_width - self.rectwidth:
            self.rectx = self.rectx - self.velx
            self.recty = self.recty + self.vely
            self.velx = -self.velx
            
        
    def draw(self,screen):
        #pygame.draw.rect(screen,(255,255,255),[self.rectx,self.recty,self.rectwidth,self.rectheight],1)
        for coordinate in self.ls:
            screen.blit(self.pic, (coordinate[0],coordinate[1]))
        
    def get_ymax(self):
        for coordinate in self.ls:
            if coordinate[1]+self.height>self.ymax:
                self.ymax = coordinate[1] + self.height
        
class bullets():
    def __init__(self, vel, colour):
        self.vel = vel
        self.width = 4
        self.height = 10
        self.ls = []
        self.colour = colour

    def move(self):
        for coordinate in self.ls:
            coordinate[1] = coordinate[1] + self.vel
            if coordinate[1]<=50 or coordinate[1]>= 575 - self.height:
                self.ls.remove(coordinate)

    def draw(self, screen):
        for coordinate in self.ls:
            pygame.draw.rect(screen,self.colour,[coordinate[0],coordinate[1]-self.height,self.width,self.height])
            

def generate_alien_bullets(time, enemylist, bulletlist):
    if time%100 ==0:
        if len(enemylist)>0:
            r = random.randint(0, len(enemylist))  #randomly choose an alien coordinate. this fixes column.
            x = enemylist[r-1][0]
            ymax = enemylist[r-1][1]
            #bullet must come from bottom of the column
            for enemy in enemylist:
                if enemy[0] == x:
                    if enemy[1]> ymax:
                        ymax = enemy[1]
            bulletlist.append([x,ymax])

            
def bullet_hit_enemy(bulletlist, enemylist, bulletwidth, bulletheight, enemywidth, enemyheight):
    global score
    for bullet in bulletlist:
        for enemy in enemylist:
            if bullet in bulletlist and enemy in enemylist:
                if abs(bullet[0] + bulletwidth/2 - (enemy[0] + enemywidth/2))<= bulletwidth/2 + enemywidth/2 and abs(bullet[1] + bulletheight/2 - (enemy[1] + enemyheight/2))<= bulletheight/2 + enemyheight/2:
                    bulletlist.remove(bullet)
                    enemylist.remove(enemy)
                    score = score + 20           

def bullet_hit_player(bulletlist, playerx, playery, bulletwidth, bulletheight, playerwidth, playerheight):
    global hearts
    for bullet in bulletlist:
        if bullet in bulletlist:
            if abs(bullet[0] + bulletwidth/2 - (playerx + playerwidth/2))<= bulletwidth/2 + playerwidth/2 and abs(bullet[1] + bulletheight/2 - (playery + playerheight/2))<= bulletheight/2 + playerheight/2:
                bulletlist.remove(bullet)
                hearts = hearts -1

def bullet_hit_bullet(lista, listb, widtha, heighta, widthb, heightb):
    for a in lista:
        for b in listb:
            if a in lista and b in listb:
                if abs(a[0] + widtha/2 - (b[0] + widthb/2))<= widtha/2 + widthb/2 and abs(a[1] + heighta/2 - (b[1] + heightb/2))<= heighta/2 + heightb/2:
                    lista.remove(a)
                    listb.remove(b)
                    
    
font = pygame.font.SysFont(None, 35)
def text_screen(text, colour, x, y):
    screen_text = font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

cannon = player(20, 20,'cannon.bmp')
aliens = alien_squad(20, 20, 'alien.png')
cannonbullets = bullets(-2, (0,255,0))
alienbullets = bullets(+2, (255,255,255))

def start():
    pygame.mixer.music.load('tune.mp3')
    pygame.mixer.music.play(-1)
    
    play = True
    while play:
        
        screen.blit(home_screen, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()

        pygame.display.update()
        clock.tick(fps)
    
    pygame.quit()
    quit()
    

def gameloop():
    play = True
    lose = False
    cannon.x = screen_width/2
    cannon.y = 525
    cannon.vel = 0
    aliens.ls = []
    aliens.rectx = 150
    aliens.recty = 50
    aliens.initialpositioning()
    aliens.ymax = aliens.recty + aliens.rectheight  
    cannonbullets.ls = []
    alienbullets.ls = []
    
    global score
    score = 0
    global hearts
    hearts = 3
    time = 0
    while play:
        if lose:
            screen.blit(lose_screen, (0, 0))
            text_screen(str(score), (255,255,255), 0.56*screen_width, 0.60*screen_height)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                        
        elif len(aliens.ls)==0:
            screen.blit(game_clear_screen, (0, 0))
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
                    if event.key == pygame.K_RIGHT:
                        cannon.vel = 5
                    elif event.key == pygame.K_LEFT:
                        cannon.vel = -5

                    if event.key == pygame.K_SPACE:
                        cannonbullets.ls.append([cannon.x, cannon.y])
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        cannon.vel = 0

            #movements and generation of enemy bullets            
            generate_alien_bullets(time, aliens.ls, alienbullets.ls)            
            cannon.move()
            aliens.move()
            aliens.get_ymax()
            cannonbullets.move()
            alienbullets.move()

            #collisions: scoring and hearts

            bullet_hit_player(alienbullets.ls, cannon.x, cannon.y, alienbullets.width, alienbullets.height, cannon.width, cannon.height)
            bullet_hit_enemy(cannonbullets.ls, aliens.ls, cannonbullets.width, cannonbullets.height, aliens.width, aliens.height)
            bullet_hit_bullet(alienbullets.ls, cannonbullets.ls, alienbullets.width, alienbullets.height, cannonbullets.width, cannonbullets.height)

            #drawing and text
            screen.fill((0,0,0))
            cannon.draw(screen)
            aliens.draw(screen)
            cannonbullets.draw(screen)
            alienbullets.draw(screen)

            
            #printing hearts, score and losing criteria
            k = 100
            for i in range(0,hearts):
                screen.blit(heart, (k,575))
                k = k + 2*heart.get_width()

            text_screen("Score: "+ str(score),(255,255,255),5,10)
            text_screen("Lives: ",(255,255,255),5,575)

            if hearts == 0 or aliens.ymax>= cannon.y:
                lose = True
                
            time = time + 1
        pygame.display.update()
        clock.tick(fps)
            
    pygame.quit()
    quit()

start()    

