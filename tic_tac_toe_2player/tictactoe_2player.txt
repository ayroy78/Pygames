#Tic Tac Toe 2 Player

import pygame
import time

pygame.init()
pygame.mixer.init()



screen_width = 600
screen_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("TIC TAC TOE 2 PLAYER")

cross = pygame.transform.scale(pygame.image.load('cross.bmp'), (int(screen_width/3), int(screen_height/4))).convert_alpha()
circle = pygame.transform.scale(pygame.image.load('circle.bmp'), (int(screen_width/3), int(screen_height/4))).convert_alpha()
tile = pygame.transform.scale(pygame.image.load('tile.bmp'), (int(screen_width/3), int(screen_height/4))).convert_alpha()

cross_top = pygame.transform.scale(pygame.image.load('cross.bmp'), (int(screen_width/2), int(screen_height/4))).convert_alpha()
circle_top = pygame.transform.scale(pygame.image.load('circle.bmp'), (int(screen_width/2), int(screen_height/4))).convert_alpha()
fps = 60
clock = pygame.time.Clock()


class tiles():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.coordinates = []

    def init(self):
        x_pos = 0
        y_pos = self.height
        for i in range(0,3):
            for j in range(0,3):
                self.coordinates.append([x_pos, y_pos,0, 0]) #(0 for unclicked, 1 for clicked;) (0 for none, 1 for cross, 2 for circle)
                x_pos = x_pos + self.width
            x_pos = 0
            y_pos = y_pos + self.height
            
    def draw(self):
        for coordinate in self.coordinates:
            if coordinate[3] == 0:
                screen.blit(tile, (coordinate[0], coordinate[1]))
            elif coordinate[3] == 1:
                screen.blit(cross, (coordinate[0], coordinate[1]))
            elif coordinate[3] ==2:
                screen.blit(circle, (coordinate[0], coordinate[1]))
            
        pygame.draw.line(screen, black, (0,150), (600, 150), width = 3)
        pygame.draw.line(screen, black, (0,300), (600, 300), width = 7)
        pygame.draw.line(screen, black, (0,450), (600, 450), width = 7)
        pygame.draw.line(screen, black, (0,600), (600, 600), width = 7)

        pygame.draw.line(screen, black, (0,150), (0, 600), width = 7)
        pygame.draw.line(screen, black, (200,150), (200, 600), width = 7)
        pygame.draw.line(screen, black, (400,150), (400, 600), width = 7)
        pygame.draw.line(screen, black, (600,150), (600, 600), width = 7)

       
board = tiles(int(screen_width/3), int(screen_height/4))

class player():
    def __init__(self, chance, icon):
        self.icon = icon #1 for cross, 2 for circle
        self.chance = chance
        self.score = 0
       
    def change_tile(self):
        if self.chance:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            for coordinate in board.coordinates: #only if the tile is unclicked should it respond, otherwise stays default and doesnt account for turn
                if coordinate[2] ==0:
                    if coordinate[0]<=mouse[0]<=coordinate[0] + tile.get_width() and coordinate[1]<=mouse[1]<=coordinate[1]+tile.get_height() and click[0]==1:
                        coordinate[2] =1
                        coordinate[3] = self.icon
                        self.chance = False
                        
    
player1 = player(False,1)        
player2 = player(False,2)

def check_win_and_draw():
    #8 ways to win, 2 for each way since cross and circle....so 16 conditionals
    #need to use elifs so that multiple points not granted!
    global win
    if board.coordinates[0][3]==1 and board.coordinates[1][3]==1 and board.coordinates[2][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (0,225), (600,225), width = 7)
        win = True
        player1.chance = True
        player2.chance = False 
    elif board.coordinates[0][3]==2 and board.coordinates[1][3]==2 and board.coordinates[2][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (0,225), (600,225), width = 7)
        win = True
        player1.chance = False
        player2.chance = True
       
        
    elif board.coordinates[0][3]==1 and board.coordinates[4][3]==1 and board.coordinates[8][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (0,150), (600,600), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[0][3]==2 and board.coordinates[4][3]==2 and board.coordinates[8][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (0,150), (600,600), width = 7)
        win = True
        player1.chance = False
        player2.chance = True
        

    elif board.coordinates[0][3]==1 and board.coordinates[3][3]==1 and board.coordinates[6][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (100,150), (100,600), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[0][3]==2 and board.coordinates[3][3]==2 and board.coordinates[6][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (0,225), (600,225), width = 7)
        win = True
        player1.chance = False
        player2.chance = True

    elif board.coordinates[1][3]==1 and board.coordinates[4][3]==1 and board.coordinates[7][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (300,150), (300,600), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[1][3]==2 and board.coordinates[4][3]==2 and board.coordinates[7][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (300,150), (300,600), width = 7)
        win = True
        player1.chance = False
        player2.chance = True

    elif board.coordinates[2][3]==1 and board.coordinates[4][3]==1 and board.coordinates[6][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (600,150), (0,600), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[2][3]==2 and board.coordinates[4][3]==2 and board.coordinates[6][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (600,150), (0,600), width = 7)
        win = True
        player1.chance = False
        player2.chance = True
       

    elif board.coordinates[2][3]==1 and board.coordinates[5][3]==1 and board.coordinates[8][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (500,150), (500,600), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[2][3]==2 and board.coordinates[5][3]==2 and board.coordinates[8][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (500,150), (500,600), width = 7)
        win = True
        player1.chance = False
        player2.chance = True

    elif board.coordinates[3][3]==1 and board.coordinates[4][3]==1 and board.coordinates[5][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (0,375), (600,375), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[3][3]==2 and board.coordinates[4][3]==2 and board.coordinates[5][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (0,375), (600,375), width = 7)
        win = True
        player1.chance = False
        player2.chance = True

    elif board.coordinates[6][3]==1 and board.coordinates[7][3]==1 and board.coordinates[8][3]==1:
        player1.score = player1.score + 1
        pygame.draw.line(screen, blue, (0,525), (600,525), width = 7)
        win = True
        player1.chance = True
        player2.chance = False
    elif board.coordinates[6][3]==2 and board.coordinates[7][3]==2 and board.coordinates[8][3]==2:
        player2.score = player2.score + 1
        pygame.draw.line(screen, red, (0,525), (600,525), width = 7)
        win = True
        player1.chance = False
        player2.chance = True

    #draw condition. If none of the above happen then win is True, gameloop entered again but no points granted.
    #The player who went second gets to go first(order shuffled), no worries...
    #it can also happen that one of the above conditions is triggered along with the below one at the same time. No panic, but saying it can happen....
    sum_clicked = 0
    for coordinate in board.coordinates:
        if coordinate[2] == 1:
            sum_clicked = sum_clicked + 1
    if sum_clicked == 9:
        win = True
        


font=pygame.font.SysFont(None, 50)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))

    
def gameloop():
    play = True
    global win
    win = False
    
    board.coordinates = []
    board.init()
    
   
    while play:
        if win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False
            time.sleep(1)
            gameloop()
            
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False

                    
            screen.fill(white)
            screen.blit(cross_top, (0,0))
            screen.blit(circle_top, (300,0))
            
            if player2.chance == False:
                player1.chance = True
                pygame.draw.rect(screen, blue, [0,0,300,150], width = 20)
            player1.change_tile()
            
            if player1.chance == False:
                player2.chance = True
                pygame.draw.rect(screen, red, [300,0,300,150], width = 20)
            player2.change_tile()

            board.draw()
            check_win_and_draw()
            
            
            text_screen(str(player1.score), black, 250,75)
            text_screen(str(player2.score), black, 325, 75)

       
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

gameloop()


