#PACMAN!!!!

import pygame
import numpy as np

pygame.init()

screen_width = 550
screen_height = 650

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


screen = pygame.display.set_mode((screen_width, screen_height))
lose_screen = pygame.transform.scale(pygame.image.load('lose_screen.bmp'), (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("PACMAN")
pygame.display.set_icon(pygame.image.load('pacman_right.bmp'))

food = pygame.transform.scale(pygame.image.load('food.bmp'), (20, 20)).convert_alpha()
energizer = pygame.transform.scale(pygame.image.load('energizer.bmp'), (20, 20)).convert_alpha()
cherry = pygame.transform.scale(pygame.image.load('cherry.bmp'), (20, 20)).convert_alpha()

fps = 60
clock = pygame.time.Clock()


class player():
    def __init__(self, width, height, pic):
        self.width = width
        self.height = height
        self.pic = [pygame.transform.scale(pygame.image.load(pic[0]), (self.width, self.height)).convert_alpha(), pygame.transform.scale(pygame.image.load(pic[1]), (self.width, self.height)).convert_alpha() , pygame.transform.scale(pygame.image.load('pacman_eat.bmp'), (20, 20)).convert_alpha()]
        self.x = 265 #initial pos
        self.y = 450
        self.velh = 0
        self.velv = 0
        self.orient = 0 # 0 for left, 1 for right
        self.eat_count = 0
        self.state = 0 # 0 for normal form, 1 for energized form

    def move(self, obstacles):
        self.x = self.x + self.velh
        self.y = self.y + self.velv

        for ob in obstacles:
            if abs(ob[0]+ob[2]/2 - (self.x + self.width/2)) < ob[2]/2 + self.width/2 and abs(ob[1]+ob[3]/2 - (self.y + self.height/2)) < ob[3]/2 + self.height/2:
                if self.velh>0: #moving to right from left side
                    self.x = ob[0] - self.width
                elif self.velh<0: #moving to left from right side
                    self.x = ob[0] + ob[2]
                elif self.velv>0: #moving down from top side
                    self.y = ob[1] - self.height
                elif self.velv<0: #moving up from bottom side
                    self.y = ob[1] + ob[3]

        #teleportation            
        if self.x<0 and 270<=self.y<= 310 - self.height:
            self.x = screen_width - self.width

        if self.x>screen_width - self.width and 270<=self.y<= 310 - self.height:
            self.x = 0
        
    def draw(self):
        if self.eat_count >= 4:
            screen.blit(self.pic[2], (self.x, self.y))
        else:
            if self.orient == 0:
                screen.blit(self.pic[0], (self.x, self.y))
            elif self.orient == 1:
                screen.blit(self.pic[1], (self.x, self.y))
        self.eat_count = self.eat_count + 1
        if self.eat_count> 7:
            self.eat_count = 0
            

pacman = player(20, 20, ['pacman_left.bmp', 'pacman_right.bmp'])

class ghost():
    def __init__(self, width, height, pic, x, y, vmag):
        self.width = width
        self.height = height
        self.pic = [pygame.transform.scale(pygame.image.load(pic[0]), (20, 20)).convert_alpha(), pygame.transform.scale(pygame.image.load(pic[1]), (20, 20)).convert_alpha()]
        self.x = x #initial positions, velocities and forms
        self.y = y
        self.vmag = vmag
        self.velh = 0
        self.velv = 0
        self.state = 1 #1 for lethal form, 0 for afraid form
        self.state_count = 0

    def check_state(self):
        if self.state == 0:
            self.state_count = self.state_count + 1
            if self.state_count > 750:
                self.state = 1
                self.state_count = 0
        
            
    #informed picking between collisions and after collision
    def pick_vel(self):
        if self.state == 1:
            if pacman.y - self.y > 20: #pacman below ghost
                self.velh = 0
                self.velv = self.vmag
            elif self.y - pacman.y > 20: #pacman above ghost
                self.velh = 0
                self.velv = -self.vmag
            elif self.x - pacman.x >0:  #pacman left of ghost
                self.velh = -self.vmag
                self.velv = 0
            else:                       #pacman right of ghost
                self.velh = self.vmag
                self.velv = 0
        elif self.state == 0:
            if pacman.y - self.y > 20: #pacman below ghost
                self.velh = 0
                self.velv = -self.vmag
            elif self.y - pacman.y > 20: #pacman above ghost
                self.velh = 0
                self.velv = self.vmag
            elif self.x - pacman.x >0: #pacman left of ghost
                self.velh = self.vmag
                self.velv = 0
            else:
                self.velh = -self.vmag #pacman right of ghost
                self.velv = 0
            
        
    #random picking upon collision
          
    def pick_vel_col(self, direc):
        #cant go: right on 0, left on 1, down on 2, up on 3
        r = np.random.random()
        if direc == 0:
            if r<=0.33:
                self.velh = -self.vmag
                self.velv = 0
            elif 0.33<r<=0.66:
                self.velh = 0
                self.velv = -self.vmag
            elif 0.66<r:
                self.velh = 0
                self.velv = self.vmag
        if direc == 1:
            if r<=0.33:
                self.velh = self.vmag
                self.velv = 0
            elif 0.33<r<=0.66:
                self.velh = 0
                self.velv = -self.vmag
            elif 0.66<r:
                self.velh = 0
                self.velv = self.vmag
        if direc == 2:
            if r<=0.33:
                self.velh = -self.vmag
                self.velv = 0
            elif 0.33<r<=0.66:
                self.velh = self.vmag
                self.velv = 0
            elif 0.66<r:
                self.velh = 0
                self.velv = -self.vmag
        if direc == 3:
            if r<=0.33:
                self.velh = -self.vmag
                self.velv = 0
            elif 0.33<r<=0.66:
                self.velh = self.vmag
                self.velv = 0
            elif 0.66<r:
                self.velh = 0
                self.velv = self.vmag
        
       
    def move(self, obstacles, time):
        if time%30 == 0:
            self.pick_vel()
        self.x = self.x + self.velh
        self.y = self.y + self.velv

        for ob in obstacles:
            if abs(ob[0]+ob[2]/2 - (self.x + self.width/2)) < ob[2]/2 + self.width/2 and abs(ob[1]+ob[3]/2 - (self.y + self.height/2)) < ob[3]/2 + self.height/2:
                if self.velh>0: #moving to right from left side
                    self.x = ob[0] - self.width
                    self.pick_vel_col(0)
                elif self.velh<0: #moving to left from right side
                    self.x = ob[0] + ob[2]
                    self.pick_vel_col(1)
                elif self.velv>0: #moving down from top side
                    self.y = ob[1] - self.height
                    self.pick_vel_col(2)
                elif self.velv<0: #moving up from bottom side
                    self.y = ob[1] + ob[3]
                    self.pick_vel_col(3)
     
        #teleportation            
        if self.x<0 and 270<=self.y<= 310 - self.height:
            self.x = screen_width - self.width

        if self.x>screen_width - self.width and 270<=self.y<= 310 - self.height:
            self.x = 0

    def draw(self):
        if self.state == 1:
            screen.blit(self.pic[0], (self.x, self.y))
        elif self.state == 0:
            screen.blit(self.pic[1], (self.x, self.y))
        

blinky = ghost(20, 20, ['blinky.bmp', 'afraid.bmp'],200,290 ,1.5)
pinky = ghost(20, 20, ['pinky.bmp', 'afraid.bmp'],240, 300, 1.25)
inky = ghost(20, 20, ['inky.bmp', 'afraid.bmp'],280,290 ,1.00 )
clyde = ghost(20, 20, ['clyde.bmp', 'afraid.bmp'],320, 300, 0.80 )

ghosts = [blinky, pinky, inky, clyde]
        
#rectangles with [x, y, width, height]
labyrynth =np.array([[25 ,50 ,500,15],   #top
            [267.5,65 ,15 ,130 - 65],
            [25 ,65 , 15, 210 - 65],
            [510,65, 15, 210 - 65],
            
            [25, 210, 75, 5],
            [95, 215, 5, 35+15],
            [0, 250+15, 100, 5],
            [450,210 , 75,5],  #corner top
            [450, 215, 5, 35+15],
            [450, 250+15, 100, 5],

            [70, 90, 50, 40],
            [160, 90, 70, 40],  #top boxes
            [430, 90, 50, 40],
            [320, 90, 70, 40],

            [70, 167.5, 50, 5],
            [430, 167.5, 50, 5],#top bars
            
            [160, 167.5, 5, 255 - 167.5],
            [165, 211.25, 35, 5],
            [390, 167.5, 5, 255 - 167.5],
            [355, 211.25, 35, 5],
            [195, 167.5, 355 - 195, 5],
            [267.5, 172.5, 5, 211.25 - 172.5],

            #[195, 285, 5, 325 - 285], #ghost box
            #[350, 285, 5, 325 - 285],
            [200, 255,350-200,5],         
            [200, 320, 350 - 200,5],

            [0, 325-15, 100, 5],#bottom corners
            [95, 330-15, 5, 35+15],
            [25, 365, 75, 5],
            [450, 325-15, 100, 5],
            [450, 330-15, 5, 35+15],
            [450, 365, 75, 5],

            [160, 325, 5, 370 - 325], #bottom bars next to corners, first 1/3rd
            [390, 325, 5, 370 - 325],
            [195, 370, 355-195, 5],
            [272.5, 375, 5, 420 -370],

            [95, 420, 120-95, 5], #bottom bars second 1/3rd
            [115, 425, 5, 470-420],
            [160, 420, 195-165, 5],
            [355, 420, 390-355, 5],
            [430, 420, 455-430, 5],
            [430, 425, 5, 470-420],

            [195, 470, 355-195,5], #bottom bars last 1/3rd
            [272.5, 470+5, 5, 520-475],
            [160,470, 5, 520-470],
            [95,520, 195-95,5],
            [390, 470, 5, 520-470],
            [355, 520, 455-355, 5],

            [25, 370, 15, 560 - 370],
            [40, 470, 75-40, 5],
            [510, 370, 15, 560 - 370],
            [475, 470, 510 - 475, 5],
            [25 ,560,500,15]          #bottom
            ])

def draw_obstacles(obstacles):
    for ob in obstacles:
        pygame.draw.rect(screen, blue, [ob[0],ob[1], ob[2], ob[3]])
        
def draw_food(food_list):
    for pellet in food_list:
        screen.blit(food, (pellet[0],pellet[1]))
        
def draw_energizer(energizer_list):
    for pellet in energizer_list:
        screen.blit(energizer, (pellet[0], pellet[1]))
        
def check_eat(food_list, energizer_list):
    #removes items from list and sets ghost.state = 0
    #if all items eaten, then level up!
    
    global score
    global level
    
    if len(food_list)>0:
        for pellet in food_list:
            if abs(pellet[0] + 10 - (pacman.x + pacman.width/2))<= 10 +pacman.width/2 and abs(pellet[1] + 10 - (pacman.y + pacman.height/2))<= 10 +pacman.height/2:
                score = score + 10
                food_list.remove(pellet)
                
    if len(energizer_list)>0:            
        for pellet in energizer_list:
            if abs(pellet[0] + 10 - (pacman.x + pacman.width/2))<= 10 +pacman.width/2 and abs(pellet[1] + 10 - (pacman.y + pacman.height/2))<= 10 +pacman.height/2:
                score = score + 10
                energizer_list.remove(pellet)
                blinky.state = 0
                pinky.state = 0
                inky.state = 0
                clyde.state = 0
                blinky.state_count,pinky.state_count, inky.state_count,clyde.state_count = 0,0,0,0

        
def ghost_pacman(ghost_list):
    global score
    global hearts
    #if ghost.state = 1 and they collide, pacman loses life and respawns at starting spot
    #if ghost.state = 0 and they collide, pacman gains extra points and ghost respwans at starting spot
    for item in ghost_list:
        if abs(item.x + item.width/2 - (pacman.x + pacman.width/2))<= item.width/2 +pacman.width/2 and abs(item.y + item.height/2 - (pacman.y + pacman.height/2))<= item.height/2 +pacman.height/2:
            if item.state == 1:
                hearts = hearts - 1
                pacman.x = 265
                pacman.y = 450
                blinky.x, blinky.y = 200,290
                pinky.x, pinky.y = 240, 300
                inky.x, inky.y = 280, 290
                clyde.x, clyde.y = 320, 300
                
            if item.state == 0:
                score = score + 100
                item.x = 260
                item.y = 290
                item.state = 1
            

font=pygame.font.SysFont(None, 40)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

def draw_lives(hearts):
    x_pos = 40
    for i in range(0, hearts):
        screen.blit(pacman.pic[0], (x_pos, 600))
        x_pos = x_pos + 30

def draw_cherries(level):
    x_pos = 490
    for i in range(0, level):
        screen.blit(cherry, (x_pos, 600))
        x_pos = x_pos - 30
        
score = 0
level = 1
hearts = 5

#gameloop is the code for between levelups,  or play agains from lose screen
def gameloop():
    play = True
    lose = False
    levelup = False
    
    time = 0
    global score
    global level
    global hearts

    pacman.x = 265 #initial pos
    pacman.y = 450
    pacman.velh = 0
    pacman.velv = 0
    pacman.orient = 0 # 0 for left, 1 for right
    pacman.eat_count = 0
    pacman.state = 0 # 0 for normal form, 1 for energized form

    blinky.x, blinky.y,  pinky.x, pinky.y,inky.x, inky.y, clyde.x, clyde.y = 200,290, 240, 300, 280, 290, 320, 300
    blinky.state, pinky.state, inky.state, clyde.state = 1,1,1,1
    blinky.state_count, pinky.state_count, inky.state_count, clyde.state_count = 0,0,0,0

    foods = [
[45, 65], [75, 65], [105, 65], [135, 65], [165, 65], [195, 65], [225, 65], [305, 65], [335, 65], [365, 65], [395, 65], [425, 65], [455, 65], [485, 65],
[135, 95],[240, 95],[290, 95], [400, 95],
[45, 135], [75, 135], [105, 135], [135, 135], [165, 135], [195, 135], [225, 135], [265, 135],[305, 135], [335, 135], [365, 135], [395, 135], [425, 135], [455, 135], [485, 135],
[45, 180], [75, 180], [105, 180], [135, 180], [165, 180], [195, 180], [225, 180], [305, 180], [335, 180], [365, 180], [395, 180],[425, 180], [455, 180], [485, 180],
[105, 220],[135, 220], [395, 220], [425, 220],
[105, 250],[135, 250], [395, 250], [425, 250],
[105, 280],[135, 280], [395, 280], [425, 280],
[105, 310],[135, 310], [395, 310], [425, 310],
[105, 340],[135, 340], [395, 340], [425, 340],
[45, 375], [75, 375], [105, 375], [135, 375], [165, 375], [195, 375], [225, 375], [305, 375], [335, 375], [365, 375], [395, 375],[425, 375], [455, 375], [485, 375],
[45, 395], [75, 395], [105, 395], [135, 395], [165, 395], [195, 395], [225, 395], [305, 395], [335, 395], [365, 395], [395, 395],[425, 395], [455, 395], [485, 395],
[75, 425], [135, 425], [165, 425], [195, 425], [225, 425], [225, 425], [265, 425], [305, 425], [335, 425], [365, 425], [395, 425], [455, 425],
[45, 445],[75, 445], [135, 445], [165, 445], [195, 445], [225, 445], [225, 445], [305, 445], [335, 445], [365, 445], [395, 445], [455, 445], [485, 445],
[45, 475], [75, 475], [105, 475], [135, 475],[165, 475], [195, 475], [225, 475], [305, 475], [335, 475], [365, 475], [395, 475],[425, 475], [455, 475], [485, 475],
[45, 495], [75, 495], [105, 495], [135, 495],[165, 495], [195, 495], [225, 495], [305, 495], [335, 495], [365, 495], [395, 495], [425, 495],[455, 495], [485, 495],            
[45, 530], [75, 530], [105, 530], [135, 530], [165, 530], [195, 530], [225, 530], [265, 530],[305, 530], [335, 530], [365, 530], [395, 530], [425, 530], [455, 530], [485, 530]
        ]

    energizers = [[45, 95],[485, 95], [45, 425], [485, 425]]

    while play:
        if lose:
            screen.blit(lose_screen, (0, 0))
            text_screen(str(score), white, 240, 433)

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        score = 0
                        hearts = 5
                        level = 1
                        gameloop()
        elif levelup:
            gameloop()
            
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pacman.velh = 1.5
                        pacman.velv = 0
                        pacman.orient = 1
                    if event.key == pygame.K_LEFT:
                        pacman.velh = -1.5
                        pacman.velv = 0
                        pacman.orient = 0
                    if event.key == pygame.K_UP:
                        pacman.velv = -1.5
                        pacman.velh = 0
                    if event.key == pygame.K_DOWN:
                        pacman.velv = 1.5
                        pacman.velh = 0
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        pacman.velh = 0
                    if event.key == pygame.K_LEFT:
                        pacman.velh = 0
                    if event.key == pygame.K_UP:
                        pacman.velv = 0
                    if event.key == pygame.K_DOWN:
                        pacman.velv = 0

            pacman.move(labyrynth)
            check_eat(foods, energizers)
            blinky.check_state()
            pinky.check_state()
            inky.check_state()
            clyde.check_state()
            
            blinky.move(labyrynth, time)
            pinky.move(labyrynth, time)
            inky.move(labyrynth, time)
            clyde.move(labyrynth, time)

            ghost_pacman(ghosts)
            
            screen.fill(black)
            draw_obstacles(labyrynth)
            draw_food(foods)
            draw_energizer(energizers)
            pacman.draw()
            blinky.draw()
            pinky.draw()
            inky.draw()
            clyde.draw()
            time = time +1

            text_screen('Score: '+ str(score), white, 40, 0)
            draw_lives(hearts)
            draw_cherries(level)

            if len(foods)==0 and len(energizers)==0:
                level = level +1
                levelup = True
            
            if hearts == 0:
                lose = True
            
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

gameloop()
        
