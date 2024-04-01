#FLAPPY BIRD. V2.0

import pygame
import random

pygame.init()
pygame.mixer.init()

screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FLAPPY BIRD")

ground_y = int(4*screen_height/5)
pipe_w = int(screen_width/8)
pipe_h = int(screen_height/2)
pipe_gap = int(screen_height/7)

background = pygame.transform.scale(pygame.image.load('background.png'),(screen_width*2,screen_height)).convert_alpha()
game_over = pygame.transform.scale(pygame.image.load('game_over.png'),(screen_width,screen_height)).convert_alpha()
home = pygame.transform.scale(pygame.image.load('home.png'),(screen_width,screen_height)).convert_alpha()

ground = pygame.transform.scale(pygame.image.load('ground.png'),(screen_width*2,ground_y)).convert_alpha()
pipe_up = pygame.transform.scale(pygame.image.load('pipe_up.png'),(pipe_w,pipe_h)).convert_alpha()
pipe_down = pygame.transform.scale(pygame.image.load('pipe_down.png'),(pipe_w,pipe_h)).convert_alpha()

pygame.mixer.Sound('point.wav')
pygame.mixer.Sound('hit.wav')

fps = 60
clock = pygame.time.Clock()

class player():
    def __init__(self,height, width, pic):
        self.height = height
        self.width = width
        self.pic = [pygame.transform.scale(pygame.image.load(pic[0]),(self.width,self.height)).convert_alpha(),
                    pygame.transform.scale(pygame.image.load(pic[1]),(self.width,self.height)).convert_alpha(),
                    pygame.transform.scale(pygame.image.load(pic[2]),(self.width,self.height)).convert_alpha(),
                    pygame.transform.scale(pygame.image.load(pic[3]),(self.width,self.height)).convert_alpha()]
        self.x = self.width
        self.y = ground_y - self.height
        self.jumpcount = 0
        self.piccount = 0
            
    def move(self):
        if self.jumpcount>=0:
            self.y = self.y + ((self.jumpcount)**2.0)/300  
        if self.jumpcount<0:
            self.y = self.y - ((self.jumpcount)**2.0)/5

        self.jumpcount = self.jumpcount + 1
            
        #bird can't exit the screen yo!!
        if self.y>= ground_y - self.height:
            self.y = ground_y - self.height
        if self.y <= 0:
            self.y = 0
        
def draw_player(screen,ob):
    if 0<=ob.piccount<=2:
        screen.blit(ob.pic[0],(ob.x,ob.y))
    if 3<=ob.piccount<=5:
        screen.blit(ob.pic[1],(ob.x,ob.y))
    if 5<=ob.piccount<=7:
        screen.blit(ob.pic[2],(ob.x,ob.y))
    if 7<=ob.piccount<=9:
        screen.blit(ob.pic[3],(ob.x,ob.y))
    ob.piccount = ob.piccount + 1
    if ob.piccount>9:
        ob.piccount = 0
    
    #For checking boundary
    #pygame.draw.rect(screen,(255,0,0),[ob.x,ob.y,ob.width,ob.height],1)
                    
def draw_pipes(screen, pipelist):
    for pipe in pipelist:
        screen.blit(pipe_up, (pipe[1]+screen_width,pipe[0]))
        screen.blit(pipe_down, (pipe[1]+screen_width,pipe[0]+pipe_h+pipe_gap))
        pipe[1] = pipe[1] - 1
        if pipe[1]+screen_width<-5*pipe_w:
            pipelist.remove(pipe)
      

font=pygame.font.SysFont(None, 35)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

  
bird = player(30, 30, ['bird_fly_1.png', 'bird_fly_2.png', 'bird_fly_3.png', 'bird_fly_4.png'])

def start():
    pygame.mixer.music.load('tune.mp3')
    pygame.mixer.music.play(-1)
    play = True
    while play:
        screen.blit(home, (0,0))
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                play = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
        pygame.display.update()
        clock.tick(fps)
            
    pygame.quit()
    quit()
    

def main():
    pygame.mixer.music.load('tune.mp3')
    pygame.mixer.music.play(-1)
    
    play = True
    lose = False
    i = 0 #this scrolls the background
    k = 0 #this outputs pipes
    score = 0
    pipes = []  #stores pipe-pair locations on the screen; also deletes them once they move left of the screen
    pipes_to_score = []
    
    #re-initialize for next try of the user
    bird.x = bird.width
    bird.y = ground_y - bird.height
    bird.jumpcount = 0
    bird.piccount = 0
    
    while play:
        if lose:
            screen.blit(game_over, (0,0))
            text_screen("Score: " + str(score), (255,0,0), int(screen_width/2.5),int(screen_height/3) )
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
                    if event.key == pygame.K_UP:
                        bird.jumpcount = -6
                 

            bird.move()

            #scrolling background    
            screen.blit(background,(i,0))
            screen.blit(background,(i+screen_width*2,0))
            i = i-1
            if i+screen_width*2==0:
                i = 0
            
            #pipes drawn first so that ground can overlap the lower pipe
            #choosing an appropriate timing to create more pipes. Selected by trial and error...
            if abs(k)%150==0:
                r1 = random.randint(int(-pipe_h/2.5) , 0)   #y-position, from highest possible to lowest for the upper pipe
                pipes.append([r1,0])
                pipes_to_score.append(0)


            draw_pipes(screen,pipes)
            k = k+1

            screen.blit(ground, (i,ground_y))
            screen.blit(ground, (i+screen_width*2,ground_y))
            
            draw_player(screen,bird)

            #check if you have hit the pipe
            for pair in pipes:
                if abs((pair[1] + screen_width + pipe_w/2) - (bird.x + bird.width/2))<= pipe_w/2 + bird.width/2 and (bird.y <= pair[0] + pipe_h or bird.y +bird.height>= pair[0]+pipe_h+pipe_gap):
                    lose = True
                    pygame.mixer.Sound.play(pygame.mixer.Sound('hit.wav'))
                    pygame.mixer.music.unload()
                    

            #scoring
            for s in range(len(pipes_to_score)-1,-1,-1):
                pipes_to_score[s] = pipes_to_score[s] -1
                if pipes_to_score[s] + screen_width + pipe_w <= bird.x:
                    pipes_to_score.pop(s)
                    score = score + 1
                    
                    
                    pygame.mixer.Sound.play(pygame.mixer.Sound('point.wav'))
                   
                    
            text_screen("Score: " + str(score), (255,0,0), 10,10 )
            
            
        pygame.display.update()
        clock.tick(fps)
            
    pygame.quit()
    quit()
    

start()


