#Voltorb Flip!!!! (A cross between picross and minesweeper apparently)

import pygame
import random
import time

pygame.mixer.init()

pygame.init()

screen_width = 600
screen_height = 600

black = (0,0,0)
red = (255, 0, 0)
white = (255, 255, 255)
bg = (0, 120, 30)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Voltorb Flip")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('zero.bmp'), (32, 32)).convert_alpha())

zero = pygame.transform.scale(pygame.image.load('zero.bmp'), (70, 70)).convert_alpha()
one = pygame.transform.scale(pygame.image.load('one.bmp'), (70, 70)).convert_alpha()
two = pygame.transform.scale(pygame.image.load('two.bmp'), (70, 70)).convert_alpha()
three = pygame.transform.scale(pygame.image.load('three.bmp'), (70, 70)).convert_alpha()
side_tile = pygame.transform.scale(pygame.image.load('side_tile.bmp'), (70, 70)).convert_alpha()

pygame.mixer.music.load('tune.mp3')
explosion = pygame.mixer.Sound('explosion.mp3')
point = pygame.mixer.Sound('point.mp3')
lvlup = pygame.mixer.Sound('lvlup.mp3')

fps = 60
clock = pygame.time.Clock()

font_level = pygame.font.SysFont(None, 50)
font_side_tile = pygame.font.SysFont(None, 30)
font_levelup = pygame.font.SysFont(None, 50)

def text_screen(text, colour, font, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))
    

class flip_tiles():
    def __init__(self, width, height, pic):
        #individual properties
        self.width = width
        self.height = height
        self.pic = pygame.transform.scale(pygame.image.load(pic), (self.width, self.height)).convert_alpha()
        
        #group properties
        self.coordinates = []
        self.indices = [i for i in range(0,25)]
        self.zerohor = [0,0,0,0,0]
        self.sumhor = [0,0,0,0,0]
        self.zerover = [0,0,0,0,0]
        self.sumver = [0,0,0,0,0]

        #level-based
        #'level' = [numzero, numtwo, numthree, numone], sum up to 25
        #accessed by self.level["levelnumber"]
        self.level = {
            "1": [6, 2, 2, 15],
            "2": [7, 3, 2, 13],
            "3": [8, 4, 2, 11],
            "4": [9, 3, 3, 10],
            "5": [10, 4, 3, 8],
            "6": [11, 5, 3, 6],
            "7": [12, 5, 4, 4]
        }
        
    def init_coordinates(self):
        xpos = 50
        ypos = 50
        for i in range(0,5):
            for k in range(0,5):
                self.coordinates.append([0,xpos,ypos])
                xpos = xpos + self.pic.get_width() + 12.5
            xpos = 50
            ypos = ypos + self.pic.get_height() + 12.5

    def level_matrix(self, level):
        numzero = self.level[level][0]
        numtwo = self.level[level][1]
        numthree = self.level[level][2]
        numone = self.level[level][3]
        
        for i in range(0,numzero):
            r = random.randint(0,len(self.indices)-1)
            self.coordinates[self.indices[r]].append(0)
            self.indices.pop(r)

        for i in range(0,numtwo):
            r = random.randint(0,len(self.indices)-1)
            self.coordinates[self.indices[r]].append(2)
            self.indices.pop(r)

        for i in range(0,numthree):
            r = random.randint(0,len(self.indices)-1)
            self.coordinates[self.indices[r]].append(3)
            self.indices.pop(r)
            
        for i in range(0,len(self.indices)):
            self.coordinates[self.indices[i]].append(1)

    def side_tiles(self):
        #horizontal sums
        count = 0
        x_pos = 50 + self.pic.get_width()*5 + 12.5*5
        y_pos = 50
        
        for i in range(0,5): #each row
            for k in range(count,count + 5): #element of a row
                self.sumhor[i] = self.sumhor[i] + self.coordinates[k][3]
                if self.coordinates[k][3] == 0:
                    self.zerohor[i] = self.zerohor[i] + 1

            y_pos = y_pos + side_tile.get_height() + 12.5
            count = count + 5
        

        #vertical sums
        count = 0
        y_pos = 50 + self.pic.get_height()*5 + 12.5*5
        x_pos = 50
        for i in range(0,5):
            for k in range(count, count + 21, 5):
                self.sumver[i] = self.sumver[i] + self.coordinates[k][3]
                if self.coordinates[k][3] == 0:
                    self.zerover[i] = self.zerover[i] + 1
                    
            x_pos = x_pos + side_tile.get_width() + 12.5
            count = count + 1
            
    def side_tiles_draw(self):
        
        x_pos = 50 + self.pic.get_width()*5 + 12.5*5
        y_pos = 50
        for i in range(0,5):
            screen.blit(side_tile, (x_pos, y_pos))
            text_screen(str(self.sumhor[i]), white, font_side_tile, x_pos + self.pic.get_width()*3/4, y_pos + self.pic.get_height()/8)
            text_screen(str(self.zerohor[i]), white, font_side_tile, x_pos + self.pic.get_width()*3/4, y_pos + self.pic.get_height()/2 + self.pic.get_height()/6)
            y_pos = y_pos + side_tile.get_height() + 12.5

        y_pos = 50 + self.pic.get_height()*5 + 12.5*5
        x_pos = 50
        for i in range(0,5):
            screen.blit(side_tile, (x_pos, y_pos))
            text_screen(str(self.sumver[i]), white, font_side_tile, x_pos + self.pic.get_width()*3/4, y_pos + self.pic.get_height()/8)
            text_screen(str(self.zerover[i]), white, font_side_tile, x_pos + self.pic.get_width()*3/4, y_pos + self.pic.get_height()/2 + self.pic.get_height()/6)
            x_pos = x_pos + side_tile.get_width() + 12.5
        
    def flip_and_draw(self):
        global lose
        global score
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for coordinate in self.coordinates:
            #interaction
            if (coordinate[1] <= mouse[0] <= coordinate[1] + self.pic.get_width() and coordinate[2] <= mouse[1] <= coordinate[2] + self.pic.get_height()):
                
                if coordinate[0] == 0: #unclicked
                    pygame.draw.rect(screen, red, [coordinate[1], coordinate[2], self.pic.get_width(), self.pic.get_height()])
                    
                   
                if coordinate[0] == 0 and click[0] ==1: #first time click, set to 1 right away so you cant interact again
                    coordinate[0] =1 
                    if coordinate[3] == 0:
                        screen.blit(zero, (coordinate[1], coordinate[2]))
                        score = score * 0
                        pygame.mixer.Sound.play(explosion)
                        lose = True
                    elif coordinate[3] == 1:
                        screen.blit(one, (coordinate[1], coordinate[2]))
                        score = score * 1
                        pygame.mixer.Sound.play(point)
                    elif coordinate[3] == 2:
                        screen.blit(two, (coordinate[1], coordinate[2]))
                        score = score * 2
                        pygame.mixer.Sound.play(point)
                    elif coordinate[3] == 3:
                        screen.blit(three, (coordinate[1], coordinate[2]))
                        score = score * 3
                        pygame.mixer.Sound.play(point)
                        
                if coordinate[0] ==1: #interactions after click
                    if coordinate[3] == 0:
                        screen.blit(zero, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 1:
                        screen.blit(one, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 2:
                        screen.blit(two, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 3:
                        screen.blit(three, (coordinate[1], coordinate[2]))
                    
            #no interaction        
            else:

                if coordinate[0] == 0: #if it has not been clicked before, then it returns to unflipped state
                    screen.blit(self.pic, (coordinate[1], coordinate[2]))

                elif coordinate[0] == 1: #it it has been clicked, it needs to blit the value to the screen
                    if coordinate[3] == 0:
                        screen.blit(zero, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 1:
                        screen.blit(one, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 2:
                        screen.blit(two, (coordinate[1], coordinate[2]))
                    elif coordinate[3] == 3:
                        screen.blit(three, (coordinate[1], coordinate[2]))

    def check_win(self, score, level):
        global win
        if score == (2**self.level[level][1])*(3**self.level[level][2]):
            win = True
            pygame.mixer.Sound.play(lvlup)
                    

cards = flip_tiles(70, 70, 'unflipped.bmp')
        
level = 1

pygame.mixer.music.play(-1)

def gameloop():
    
   
    play = True

    global lose
    lose = False

    global win
    win = False

    global level
    
    global score
    score = 1

    cards.coordinates = []
    cards.indices = [i for i in range(0,25)]
    cards.zerohor = [0,0,0,0,0]
    cards.sumhor = [0,0,0,0,0]
    cards.zerover = [0,0,0,0,0]
    cards.sumver = [0,0,0,0,0]
    
    cards.init_coordinates()
    cards.level_matrix(str(level))
    cards.side_tiles()
    
    while play:   
        if lose:
            text_screen('YOU PICKED VOLTORB!', white, font_levelup, screen_width/4,0 )
            pygame.display.update()
            clock.tick(fps)
            time.sleep(1.5)
            for coordinate in cards.coordinates:
                if coordinate[3] == 0:
                    screen.blit(zero, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 1:
                    screen.blit(one, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 2:
                    screen.blit(two, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 3:
                    screen.blit(three, (coordinate[1], coordinate[2]))
            pygame.display.update()
            clock.tick(fps)
            time.sleep(4)
            if level == 1:
                gameloop()
            if level>1:
                level = level -1
                gameloop()
            
        elif win:
            text_screen('LEVEL CLEARED!', white, font_levelup, screen_width/4,0 )
            pygame.display.update()
            clock.tick(fps)
            time.sleep(1.5)
            for coordinate in cards.coordinates:
                if coordinate[3] == 0:
                    screen.blit(zero, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 1:
                    screen.blit(one, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 2:
                    screen.blit(two, (coordinate[1], coordinate[2]))
                elif coordinate[3] == 3:
                    screen.blit(three, (coordinate[1], coordinate[2]))
            pygame.display.update()
            clock.tick(fps)
            time.sleep(4)
            if level<=6:
                level = level +1
                gameloop()
            if level ==7:
                screen.fill(bg)
                text_screen('GAME CLEARED', white, font_level, screen_width/8,screen_height/2 )
                text_screen('Press Spacebar to Play Again', white, font_level, screen_width/8,screen_height*3/4 )
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            level = 1
                            gameloop()
                pygame.display.update()
                clock.tick(fps)           
                
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False
                    
        screen.fill(bg)
        cards.side_tiles_draw()
        
        cards.flip_and_draw()
        text_screen('Level: '+str(level), white, font_level, 400,550 )
        cards.check_win(score, str(level))
      
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
    
gameloop()

