#Classic snake eats apple biblical game

import pygame
import random

pygame.mixer.init()

pygame.init()

# Colours

red = (255, 0, 0)
green=(0,255,0)
black = (0, 0, 0)
white = (255, 255, 255)


# Creating game window and game title
screen_width = 500
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakeEatsApple")

welcome_screen = pygame.image.load("welcome_screen.jpg")
welcome_screen = pygame.transform.scale(welcome_screen, (screen_width, screen_height)).convert_alpha()

game_screen = pygame.image.load("game_screen.jpg")
game_screen = pygame.transform.scale(game_screen, (screen_width, screen_height)).convert_alpha()

game_over_screen = pygame.image.load("game_over_screen.jpg")
game_over_screen = pygame.transform.scale(game_over_screen, (screen_width, screen_height)).convert_alpha()



#control frame rate
fps = 60
clock = pygame.time.Clock()


#For printing text to the game window
font=pygame.font.SysFont(None, 25)
def text_screen(text, colour, x, y):
    screen_text=font.render(text,True,colour)
    gameWindow.blit(screen_text,(x,y))

#for plotting snake
def plot_snake(gameWindow,colour,lst,size):
    for x,y in lst:
        pygame.draw.rect(gameWindow, colour, [x, y, size, size])

#welcome screen    
def welcome():
    exit_game = False
    while not exit_game:
        
        gameWindow.blit(welcome_screen, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('naagin.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()

        pygame.display.update()
        clock.tick(fps)
    #REQUIRED so that pygame quits
    pygame.quit()
    quit()

#the game        
def gameloop():
    # Game specific variables
    exit_game = False  #if the user wants to quit the game
    game_over = False  #if the snake eats itself or hits the wall
    snake_x = 45       #initial position of the snake
    snake_y = 55
    velocity_x = 0     #speed of the snake
    velocity_y = 0

    food_x = random.randint(int(screen_width*(1/5)), int(screen_width*(4/5)))
    food_y = random.randint(int(screen_width*(1/5)), int(screen_height*(4/5)))
    score = 0
    init_velocity = 3.5  #can increase to increase difficulty
    snake_size = 15 #the rectangular block size of the snake 
    snake_list=[]   #stores coordinates of snake's head
    snake_length=1  #stores length of the snake
    apple=pygame.image.load("apple.jpg")

    
    # Game Loop
    while not exit_game:   #as long as the user does not hit quit, this loop runs
        if game_over:
            gameWindow.blit(game_over_screen, (0, 0))

            for event in pygame.event.get(): #all the user-input events
                if event.type == pygame.QUIT:  #quits the game from game over window
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('naagin.mp3')
                        pygame.mixer.music.play(-1)
                        gameloop()
                
                
                        
        else:
            for event in pygame.event.get(): #all the user-input events
                if event.type == pygame.QUIT:  #quits the game from live game window
                    exit_game = True

                if event.type == pygame.KEYDOWN:  #key-stroke events
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y


            #to check if snake eats apple, increasing snake length and the score
            if abs(snake_x - food_x)<=(2/3)*snake_size and abs(snake_y - food_y)<=(2/3)*snake_size:
                score = score + 1
                food_x = random.randint(int(screen_width*(1/5)), int(screen_width*(4/5)))
                food_y = random.randint(int(screen_width*(1/5)), int(screen_height*(4/5)))
                snake_length=snake_length+5


            #gameWindow.fill(white), if you want a white screen
            gameWindow.blit(game_screen, (0, 0))
            
            #draws apple and snake regardless of whether apple is eaten or not, on top of the game screen

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            #check if snake needs to be cut-off
            if len(snake_list)>snake_length:
                del snake_list[0]

            #game over conditions
            #if head(last element in snake list) is in some other element of snake list, game over     
            if head in snake_list[:-1]:
                game_over=True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            text_screen("Score: "+ str(score * 10),red,5,5) #printing score to game window
            plot_snake(gameWindow,green,snake_list,snake_size)
            apple = pygame.transform.scale(apple, (int(snake_size), int(snake_size))).convert_alpha()
            gameWindow.blit(apple, (int(food_x),int(food_y)))

        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
   
   
