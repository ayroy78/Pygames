#CLASSIC CRICKET 1.1.6

#Version 1.1.7 
#sound     
#tie and superover
    
#Version Gold Hexa Platinima
#fielders, catch out, runout

import pygame
import numpy as np
import time

pygame.init()
pygame.mixer.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Classic Cricket")
pygame.display.set_icon(pygame.image.load('rhb_cut.png'))


white = (255,255,255)
red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

#pictures
ground = pygame.transform.scale(pygame.image.load('ground.bmp'), (screen_width,screen_height )).convert_alpha()
logo = pygame.transform.scale(pygame.image.load('logo.png'), (200,150)).convert_alpha()
#right-handed batsman
rhb_stance =        pygame.transform.scale(pygame.image.load('rhb_stance.png'),(589 - 516,216 - 116)).convert_alpha() #stance
rhb_cut =           pygame.transform.scale(pygame.image.load('rhb_cut.png'),(589 - 480,216 - 116)).convert_alpha() #cut
rhb_offdrive =      pygame.transform.scale(pygame.image.load('rhb_offdrive.png'),(589 - 500,216 - 116)).convert_alpha() # off drive
rhb_straightdrive = pygame.transform.scale(pygame.image.load('rhb_straightdrive.png'),(589 - 516,216 - 116)).convert_alpha() #straightdrive
rhb_pull =          pygame.transform.scale(pygame.image.load('rhb_pull.png'),(589 - 480,216 - 116)).convert_alpha() #pull
rhb_ondrive =       pygame.transform.scale(pygame.image.load('rhb_ondrive.png'),(589 - 500,216 - 116)).convert_alpha() #ondrive
#left-handed batsman
lhb_stance =        pygame.transform.scale(pygame.image.load('lhb_stance.png'),(589 - 516,216 - 116)).convert_alpha() #stance
lhb_cut =           pygame.transform.scale(pygame.image.load('lhb_cut.png'),(589 - 480,216 - 116)).convert_alpha() #cut
lhb_offdrive =      pygame.transform.scale(pygame.image.load('lhb_offdrive.png'),(589 - 500,216 - 116)).convert_alpha() # off drive
lhb_straightdrive = pygame.transform.scale(pygame.image.load('lhb_straightdrive.png'),(589 - 516,216 - 116)).convert_alpha() #straightdrive
lhb_pull =          pygame.transform.scale(pygame.image.load('lhb_pull.png'),(589 - 480,216 - 116)).convert_alpha() #pull
lhb_ondrive =       pygame.transform.scale(pygame.image.load('lhb_ondrive.png'),(589 - 500,216 - 116)).convert_alpha() #ondrive
#right-handed bowler
rhb_1 =             pygame.transform.scale(pygame.image.load('rb1.png'),(111,150)).convert_alpha()
rhb_2 =             pygame.transform.scale(pygame.image.load('rb2.png'),(111,150)).convert_alpha()
rhb_3 =             pygame.transform.scale(pygame.image.load('rb3.png'),(111,150)).convert_alpha()
rhb_4 =             pygame.transform.scale(pygame.image.load('rb4.png'),(111,150)).convert_alpha()
rhb_5 =             pygame.transform.scale(pygame.image.load('rb5.png'),(111,150)).convert_alpha()
rhb_6 =             pygame.transform.scale(pygame.image.load('rb6.png'),(111,150)).convert_alpha()

rhb = [rhb_1, rhb_2, rhb_3, rhb_4, rhb_5, rhb_6]

#left-handed bowler
lhb_1 =             pygame.transform.scale(pygame.image.load('lb1.png'),(111,150)).convert_alpha()
lhb_2 =             pygame.transform.scale(pygame.image.load('lb2.png'),(111,150)).convert_alpha()
lhb_3 =             pygame.transform.scale(pygame.image.load('lb3.png'),(111,150)).convert_alpha()
lhb_4 =             pygame.transform.scale(pygame.image.load('lb4.png'),(111,150)).convert_alpha()
lhb_5 =             pygame.transform.scale(pygame.image.load('lb5.png'),(111,150)).convert_alpha()
lhb_6 =             pygame.transform.scale(pygame.image.load('lb6.png'),(111,150)).convert_alpha()

lhb = [lhb_1, lhb_2, lhb_3, lhb_4, lhb_5, lhb_6]
#umpire
ump_1 =             pygame.transform.scale(pygame.image.load('ump_stance.png'),(571 - 489, 525 - 395)).convert_alpha()
ump_2 =             pygame.transform.scale(pygame.image.load('ump_four.png'),(571 - 489, 525 - 395)).convert_alpha()
ump_3 =             pygame.transform.scale(pygame.image.load('ump_six.png'),(571 - 489, 525 - 395)).convert_alpha()
ump_4 =             pygame.transform.scale(pygame.image.load('ump_out.png'),(571 - 489, 525 - 395)).convert_alpha()
#wicketkeeper
wk_1 =              pygame.transform.scale(pygame.image.load('wk_stance.png'),(75, 75)).convert_alpha()
wk_2 =              pygame.transform.scale(pygame.image.load('wk_left.png'),(75,75)).convert_alpha()
wk_3 =              pygame.transform.scale(pygame.image.load('wk_right.png'),(75,75)).convert_alpha()

#runner
runner = pygame.transform.scale(pygame.image.load('runner.png'), (80 , 110)).convert_alpha()

#match stats
left_panel = pygame.transform.scale(pygame.image.load('left_panel.bmp'),(250,140)).convert_alpha()
right_panel = pygame.transform.scale(pygame.image.load('right_panel.bmp'),(300,140)).convert_alpha()

#match end
match_end = pygame.transform.scale(pygame.image.load('match_end.jpg'),(screen_width,screen_height)).convert_alpha()
match_end_bat = pygame.transform.scale(pygame.image.load('match_end_bat.bmp'),(340,440)).convert_alpha()
match_end_bowl = pygame.transform.scale(pygame.image.load('match_end_bowl.bmp'),(300,200)).convert_alpha()

fps = 60
clock = pygame.time.Clock()

class batsman():
    def __init__(self, name, kind):
        
        self.name = name
        self.kind = kind #0 for left-handed, 1 for right-handed
        
        self.hit = False #played a shot or not
        self.wrong = False #wrong shot
        self.shot = 0 #0 for stance, 1 for cut, 2 for offdrive, 3 for straightdrive, 4 for pull, 5 for ondrive
        
        self.runs = 0
        self.balls = 0
        
    def draw(self): #switched for left-handers
        if self.shot == 1:
            if self.kind == 1:
                screen.blit(rhb_cut, (480, 116))
            if self.kind == 0:
                screen.blit(lhb_pull, (480, 116))   
        if self.shot == 2:
            if self.kind == 1:
                screen.blit(rhb_offdrive, (500, 116))
            if self.kind == 0:
                screen.blit(lhb_ondrive, (500, 116)) 
        if self.shot == 3:
            if self.kind == 1:
                screen.blit(rhb_straightdrive, (516, 116))
            if self.kind == 0:
                screen.blit(lhb_straightdrive, (516, 116)) 
        if self.shot == 4:
            if self.kind == 1:
                screen.blit(rhb_pull, (516, 116))
            if self.kind == 0:
                screen.blit(lhb_cut, (516, 116)) 
        if self.shot == 5:
            if self.kind == 1:
                screen.blit(rhb_ondrive, (516, 116))
            if self.kind == 0:
                screen.blit(lhb_offdrive, (516, 116)) 
        if self.shot == 0:
            if self.kind == 1:
                screen.blit(rhb_stance, (516, 116))
            if self.kind == 0:
                screen.blit(lhb_stance, (516, 116)) 
        
class bowler():
    def __init__(self, name, x, y, x0, y0, kind, hand):
        self.name = name
        self.x_or = x
        self.y_or = y
        self.x = self.x_or
        self.y = self.y_or
        self.x0 = x0
        self.y0 = y0
        self.kind = kind
        self.hand = hand #0 for left, 1 for right
    
        self.count = 0
        self.run = False  #only let bowler run after space bar is hit
        self.hasrun = False #dont allow bowler to run after he has run/ space bar has been hit
        self.delivered = False
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        
    def move_and_draw(self):
        if not self.run and not self.delivered:
            if self.hand == 1:
                screen.blit(rhb[0], (self.x_or, self.y_or))
            if self.hand == 0:
                screen.blit(lhb[0], (self.x_or, self.y_or))
                 
        if self.run:
            if self.kind == 0 or self.kind == 1:  #fast bowling
                self.y = self.y - 10
                if self.hand == 1:
                    screen.blit(rhb[self.count], (self.x, self.y))
                if self.hand == 0:
                    screen.blit(lhb[self.count], (self.x, self.y)) 
                self.count = self.count + 1
                if self.count==5:
                    self.count = 0
            if self.kind == 2 or self.kind == 3: #spin bowling
                self.y = self.y - 2
                if 0<=self.count<=5:
                    if self.hand == 1:
                        screen.blit(rhb[0], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[0], (self.x, self.y))      
                if 6<=self.count<=10:
                    if self.hand == 1:
                        screen.blit(rhb[1], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[1], (self.x, self.y)) 
                if 11<=self.count<=15:
                    if self.hand == 1:
                        screen.blit(rhb[2], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[2], (self.x, self.y)) 
                if 16<=self.count<=20:
                    if self.hand == 1:
                        screen.blit(rhb[3], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[3], (self.x, self.y)) 
                if 20<=self.count<=25:
                    if self.hand == 1:
                        screen.blit(rhb[4], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[4], (self.x, self.y)) 
                if 25<=self.count<=30:
                    if self.hand == 1:
                        screen.blit(rhb[5], (self.x, self.y))
                    if self.hand == 0:
                        screen.blit(lhb[5], (self.x, self.y)) 
                self.count = self.count + 1
                if self.count==31:
                    self.count = 0
                
        if self.y<=412:
            self.run = False
            self.delivered = True
            if self.hand == 1:
                screen.blit(rhb[0], (self.x, self.y))
            if self.hand == 0:
                screen.blit(lhb[0], (self.x, self.y))
            

class wicketkeeper():
    def __init__(self):
        self.x = 520
        self.y = 50

    def draw(self, selected_bowler, ball):
        if selected_bowler.delivered:
            if ball.y<150:
                if 400<ball.x<500:
                    screen.blit(wk_2, (ball.x, self.y))
                elif 580<ball.x<650:
                    screen.blit(wk_3, (ball.x, self.y))
                else:
                    screen.blit(wk_1, (self.x, self.y))
            else:
                screen.blit(wk_1, (self.x, self.y))
                
        else:
            screen.blit(wk_1, (self.x, self.y))
                
            
class umpire():
    def __init__(self):
        self.x = 489
        self.y = 395
        
    def draw(self, action):
        if action == 4:
            screen.blit(ump_2, (self.x, self.y))
        elif action == 6:
            screen.blit(ump_3, (self.x, self.y))
        elif action == 8:
            screen.blit(ump_4, (self.x, self.y))
        else:
            screen.blit(ump_1, (self.x, self.y))
        
bat1 = batsman('R.Sharma',1)
bat2 = batsman('K.Rahul',1)
bat3 = batsman('V.Kohli',1)
bat4 = batsman('S.Yadav',1)
bat5 = batsman('R.Pant',0)
bat6 = batsman('H.Pandya',1)
bat7 = batsman('R.Jadeja',0)
bat8 = batsman('S.Thakur',1)
bat9 = batsman('W.Sundar',0)
bat10 = batsman('B.Kumar',1)
bat11 = batsman('J.Bumrah',1)


#a_bowler = bowler(run up x, deliver x0, y. y0 fixed. type(0,1,2, 3)-> this sets y and x1,y1,x2,y2 and xchange vel, handedness)

bowl1 = bowler('J.Hzlwd',363, 573, 444, 412, 0, 1)
bowl2 = bowler('P.Cumns', 363, 573, 444, 412, 1, 1)
bowl3 = bowler('M.Starc', 580, 573, 580, 412, 1, 0)
bowl4 = bowler('N.Lyon',363, 500, 444, 412, 2, 1)
bowl5 = bowler('A.Zampa', 363, 500, 444, 412, 3, 1)

wk = wicketkeeper()
ump = umpire()

batsmen = [bat1, bat2, bat3, bat4, bat5, bat6, bat7, bat8, bat9, bat10, bat11]
bowlers = [bowl1, bowl2, bowl3, bowl4, bowl5]


class ball():
    def __init__(self):
        #delivery characteristics
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.xchange1 = 0
        self.xchange2 = 0
        self.x = 0
        self.y = 0
        self.generated = False

        #batter hit charactersitics
        self.hit = False #if batsman CONNECTS, then this is True
        self.vector = (0,0)
        self.vmag = 0

    def generate_ball(self, selected_bowler, onstrike):  
        if not self.generated:
            if onstrike.kind == 1: #right-handed batsman
                if selected_bowler.kind == 0: #fast outswing bowler
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 469 + (581-469)*np.random.random()
                    self.y1 = 218 + (315 - 218)*np.random.random()
                    self.x2 = self.x1 - 25*np.random.random()
                    self.xchange1 = 0.060*(self.x1 - self.x0)
                    self.xchange2 = 0.060*(self.x2 - self.x1)
                    self.y2 = 75
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                    
                if selected_bowler.kind == 1: #fast inswing bowler
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 469 + (550-469)*np.random.random()
                    self.y1 = 218 + (315 - 218)*np.random.random()
                    self.x2 = self.x1 + 25*np.random.random()
                    self.xchange1 = 0.060*(self.x1 - self.x0)
                    self.xchange2 = 0.060*(self.x2 - self.x1)
                    self.y2 = 75
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                
                if selected_bowler.kind == 2: # right arm offspin or left arm legspin
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 469 + (540-469)*np.random.random()
                    self.y1 = 218 + (266.5 - 218)*np.random.random()
                    self.x2 = self.x1 + 80*np.random.random()
                    self.xchange1 = 0.040*(self.x1 - self.x0)
                    self.xchange2 = 0.040*(self.x2 - self.x1)
                    self.y2 = 125
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                    
                if selected_bowler.kind == 3: # right arm leg spin or left arm off spin
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 500 + (590-500)*np.random.random()
                    self.y1 = 218 + (266.5 - 218)*np.random.random()
                    self.x2 = self.x1 - 80*np.random.random()
                    self.xchange1 = 0.040*(self.x1 - self.x0)
                    self.xchange2 = 0.040*(self.x2 - self.x1)
                    self.y2 = 125
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                    
            if onstrike.kind == 0: #left-handed batsman
                if selected_bowler.kind == 0: #fast outswing bowler
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 550 + (630-550)*np.random.random()
                    self.y1 = 218 + (315 - 218)*np.random.random()
                    self.x2 = self.x1 - 25*np.random.random()
                    self.xchange1 = 0.060*(self.x1 - self.x0)
                    self.xchange2 = 0.060*(self.x2 - self.x1)
                    self.y2 = 75
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                    
                if selected_bowler.kind == 1: #fast inswing bowler
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 520 + (610-520)*np.random.random()
                    self.y1 = 218 + (315 - 218)*np.random.random()
                    self.x2 = self.x1 + 25*np.random.random()
                    self.xchange1 = 0.060*(self.x1 - self.x0)
                    self.xchange2 = 0.060*(self.x2 - self.x1)
                    self.y2 = 75
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                
                if selected_bowler.kind == 2: # right arm offspin or left arm legspin
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 520 + (610-520)*np.random.random()
                    self.y1 = 218 + (266.5 - 218)*np.random.random()
                    self.x2 = self.x1 + 80*np.random.random()
                    self.xchange1 = 0.040*(self.x1 - self.x0)
                    self.xchange2 = 0.040*(self.x2 - self.x1)
                    self.y2 = 125
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                    
                if selected_bowler.kind == 3: # right arm leg spin or left arm off spin
                    self.x0 = selected_bowler.x0
                    self.y0 = selected_bowler.y0
                    self.x1 = 550 + (630-550)*np.random.random()
                    self.y1 = 218 + (266.5 - 218)*np.random.random()
                    self.x2 = self.x1 - 80*np.random.random()
                    self.xchange1 = 0.040*(self.x1 - self.x0)
                    self.xchange2 = 0.040*(self.x2 - self.x1)
                    self.y2 = 125
                    self.x = self.x0
                    self.y = self.y0
                    self.generated = True
                
                
                
                   
    def deliver_ball(self, selected_bowler, onstrike): #this keeps the ball going and batsman miss condition.
        global balls
        if selected_bowler.delivered and not self.hit:
            
            if self.y1 < self.y <= self.y0: #before pitching
            
                pygame.draw.circle(screen, red, (self.x, self.y), self.y*0.025)
                if abs(self.y - self.y1)<= 2:  #pitch condition
                    time.sleep(0.05)
                self.x = self.x + self.xchange1
                self.y = (self.y0 - self.y1)*(self.x - self.x0)/(self.x0 - self.x1) + self.y0
                if self.y<= self.y1:
                    self.x = self.x1
                    self.y = self.y1
                
            if self.y2 <= self.y <= self.y1:
                pygame.draw.circle(screen, red, (self.x, self.y), 5)
                self.x = self.x + self.xchange2
                self.y = (self.y1 - self.y2)*(self.x - self.x1)/(self.x1 - self.x2) + self.y1
            
            #keeps on simulating after ball reaches keeper. this only happens if self.hit = False; battter makes no contact either
            #by playing correct shot and poor timing or playing the wrong shot, or also if batsman.hit = False
            if self.y <self.y2:
                selected_bowler.x = selected_bowler.x_or
                selected_bowler.y = selected_bowler.y_or
                selected_bowler.hasrun = False
                selected_bowler.delivered = False
                self.generated = False
                onstrike.hit = False
                onstrike.wrong = False
                balls = balls + 1
                selected_bowler.balls = selected_bowler.balls + 1
                onstrike.balls = onstrike.balls + 1
                time.sleep(0.10)
                
    def hit_ball(self, selected_bowler, onstrike): #if batter makes contact. ball moves past screen. need to set self.hit, brettlee.delivered and virat.hit = False, False, False as well
        global balls
        if self.hit:     
            self.x = self.x + self.vector[0]*self.vmag
            self.y = self.y + self.vector[1]*self.vmag
            pygame.draw.circle(screen, red, (self.x, self.y), 5)
            
            if self.x<0 or self.x>screen_width or self.y<0 or self.y> screen_height:     
                selected_bowler.x = selected_bowler.x_or
                selected_bowler.y = selected_bowler.y_or
                selected_bowler.hasrun = False
                selected_bowler.delivered = False
                self.generated = False
                onstrike.hit = False
                self.hit = False
                balls = balls + 1
                selected_bowler.balls = selected_bowler.balls + 1
                onstrike.balls = onstrike.balls + 1
                time.sleep(0.10)

    def lbw_bowled(self, selected_bowler, onstrike):
        #irrespective of whether shot is offered and whether it is wrong or timing is not ok, if ball collides with wickets from a certain length(y1),
        #then its a wicket
        global wickets
        global balls
        global action
        if selected_bowler.delivered and not self.hit:
            if self.y1<=267.5:
                y_perf = (116 - 216)*(self.y1 - 315)/(315 - 218) + 116
                if 535<=self.x<=575 and y_perf - self.y > 40 : #if ball is 40 or lesser than y_perf, lbw or bowled
                    selected_bowler.wickets = selected_bowler.wickets + 1
                    wickets = wickets + 1
                    action = 8
                    selected_bowler.x = selected_bowler.x_or
                    selected_bowler.y = selected_bowler.y_or
                    selected_bowler.hasrun = False
                    selected_bowler.delivered = False
                    self.generated = False
                    onstrike.hit = False   #incase shot was attempted
                    onstrike.wrong = False #incase a wrong shot was played
                    balls = balls + 1
                    selected_bowler.balls = selected_bowler.balls + 1
                    onstrike.balls = onstrike.balls + 1
                    time.sleep(0.10)
            
            
cherry = ball()

        
def select_bowler(bowlers_list, balls):
    if 0<=balls<=5 or 12<=balls<=17 or 24<=balls<=29 or 90<=balls<=95:
        return bowlers_list[0]
    if 6<=balls<=11 or 18<=balls<=23 or 78<=balls<=83 or 108<=balls<=113:
        return bowlers_list[1]
    if 30<=balls<=35 or 66<=balls<=71 or 102<=balls<=107 or 114<=balls<=119:
        return bowlers_list[2]
    if 36<=balls<=41 or 48<=balls<=53 or 60<=balls<=65 or 72<=balls<=77:
        return bowlers_list[3]
    if 42<=balls<=47 or 54<=balls<=59 or 84<=balls<=89 or 96<=balls<=101:
        return bowlers_list[4]
    

def draw_runner(selected_bowler):
    if selected_bowler.x0 <500:
        screen.blit(runner, (593,365))
    if selected_bowler.x0>500:
        screen.blit(runner, (409, 365))
        
def scoring(selected_bowler, onstrike):
    #can put wicket possibility here
    global score
    global action
    if onstrike.hit and not onstrike.wrong:
        y_perf = (116 - 216)*(cherry.y1 - 315)/(315 - 218) + 116
        if abs(cherry.y-y_perf) <= 10:
            score = score + 6
            cherry.hit = True
            cherry.vmag = 50
            action = 6
            selected_bowler.runs = selected_bowler.runs + 6
            onstrike.runs = onstrike.runs + 6
        if 10<abs(cherry.y - y_perf)<= 15:
            score = score + 4
            cherry.hit = True
            cherry.vmag = 40
            action = 4
            selected_bowler.runs = selected_bowler.runs + 4
            onstrike.runs = onstrike.runs + 4
            
        if 15<abs(cherry.y - y_perf)<= 20:
            score = score + 3
            cherry.hit = True
            cherry.vmag = 30
            action = 3
            selected_bowler.runs = selected_bowler.runs + 3
            onstrike.runs = onstrike.runs + 3
            
        if 20<abs (cherry.y - y_perf)<= 25:
            score = score +2
            cherry.hit = True
            cherry.vmag = 20
            action = 2
            selected_bowler.runs = selected_bowler.runs + 2
            onstrike.runs = onstrike.runs + 2

        if 25<abs (cherry.y - y_perf)<= 30:
            score = score +1
            cherry.hit = True
            cherry.vmag = 10
            action = 1
            selected_bowler.runs = selected_bowler.runs + 1
            onstrike.runs = onstrike.runs + 1

        if 30<abs (cherry.y - y_perf)<=40:
            score = score + 0
            cherry.hit = True
            cherry.vmag = 5
            action = 0
            
            selected_bowler.runs = selected_bowler.runs + 0
            onstrike.runs = onstrike.runs + 0

        if abs(cherry.y - y_perf) > 40: #is the miss condition after playing correct shot but not timing properly
            action = 7

   
def show_event(ball, balls): #show event on screen, change over, change strike
    global action
    global prev_stri  #previous ball, used for switching after an over is bowled
    global prev_nonstri
    global stri  #upcoming ball
    global nonstri
    
    if action != -1: 
        if action == 0 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, 'DOT', 'red', 450, 275)
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1 #back to dummy value
            
        if action == 1 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, '1', 'red', 500, 275)
            stri = prev_nonstri
            nonstri = prev_stri
            prev_nonstri = nonstri
            prev_stri = stri
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
        if action == 2 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, '2', 'red', 500, 275)
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
        if action == 3 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, '3', 'red', 500, 275)
            stri = prev_nonstri
            nonstri = prev_stri
            prev_nonstri = nonstri
            prev_stri = stri
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
        if action == 4 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, '4', 'red', 500, 275)
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
        if action == 6 and (ball.x<0 or ball.x>screen_width or ball.y<0 or ball.y> screen_height):
            text_screen(event_font, '6', 'red', 500, 275)
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
         
        if action == 7 and ball.y<ball.y2:  #poor timing, wrong shot or not attempting a shot
            text_screen(event_font, 'DOT', 'red', 450, 275)
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
        if action == 8: #if you lose a wicket, the person on strike changes to max(stri, nonstri) + 1; nonstriker remains the same
            text_screen(event_font, 'OUT!', 'red', 450, 275)
            if max(stri, nonstri)<=10:
                stri = max(stri, nonstri) + 1
                prev_stri = stri
            pygame.display.update()
            clock.tick(fps)
            time.sleep(0.75)
            if balls%6 == 0 and balls<120:
                text_screen(event_font, 'OVER UP', 'red', 820, 374)
                stri = prev_nonstri
                nonstri = prev_stri
                prev_nonstri = nonstri
                prev_stri = stri
                pygame.display.update()
                clock.tick(fps)
                time.sleep(0.75)
            action = -1
            
            
        
score_font = pygame.font.SysFont(None, 30)
event_font = pygame.font.SysFont(None, 125)

def text_screen(font, text, colour, x, y):
    screen_text=font.render(text,True,colour)
    screen.blit(screen_text,(x,y))


def draw_button(font, text, textcol, x, y, width, height, inactcol, actcol, mouse, click, kind): #0 for player choice and 1 for opponent choice
    global play_choice
    global opp_choice
    #the press condition     
    if x<mouse[0]<x+width and y<mouse[1]<y+height and click[0] == 1:  
        pygame.draw.rect(screen, actcol, [x, y, width, height])
        text_screen(font, text, textcol, x+2, y+ 2)
        if kind == 0:
            play_choice = text
        if kind == 1:
            opp_choice = text
        
    #the long term conditions
    if kind == 0:
        if play_choice == text:
            pygame.draw.rect(screen, actcol, [x, y, width, height])
            text_screen(font, text, textcol, x+2, y+ 2)  
        else:
            pygame.draw.rect(screen, inactcol, [x, y, width, height])
            text_screen(font, text, textcol, x+2, y+ 2)
            
    if kind == 1:
        if opp_choice == text:
            pygame.draw.rect(screen, actcol, [x, y, width, height])
            text_screen(font, text, textcol, x+2, y+ 2)
            
        else:
            pygame.draw.rect(screen, inactcol, [x, y, width, height])
            text_screen(font, text, textcol, x+2, y+ 2)
        

            
def homescreen():
    play = True
    global play_choice
    global opp_choice
    play_choice = 'None'
    opp_choice = 'None'
    
    while play:   
        screen.blit(ground, (0,0))
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        text_screen(score_font, 'Pick Side', black, 250, 50)
        text_screen(score_font, 'Pick Opposition', black, 600, 50)
        

        draw_button(score_font, 'IND', white, 350, 100, 150, 50, blue, red, mouse, click, 0)
        draw_button(score_font, 'AUS', white, 350, 200, 150, 50, blue, red, mouse, click, 0)
        draw_button(score_font, 'ENG', white, 350, 300, 150, 50, blue, red, mouse, click, 0)
        draw_button(score_font, 'PAK', white, 350, 400, 150, 50, blue, red, mouse, click,0)

        draw_button(score_font, 'IND', white, 750, 100, 150, 50, blue, red, mouse, click, 1)
        draw_button(score_font, 'AUS', white, 750, 200, 150, 50, blue, red, mouse, click, 1)
        draw_button(score_font, 'ENG', white, 750, 300, 150, 50, blue, red, mouse, click, 1)
        draw_button(score_font, 'PAK', white, 750, 400, 150, 50, blue, red, mouse, click, 1)

        if play_choice!= 'None' and opp_choice!='None':
            text_screen(score_font, 'Press Enter to Play', black, 500, 500)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if play_choice!= 'None' and opp_choice!='None':
                    if event.key == pygame.K_RETURN:
                        gameloop()

        pygame.display.update()
        clock.tick(fps)
    #REQUIRED so that pygame quits
    pygame.quit()
    quit()
    
def gameloop():
    #team members on both sides
    
    if play_choice == 'IND':
        batsmen[0].name, batsmen[1].name, batsmen[2].name, batsmen[3].name, batsmen[4].name, batsmen[5].name = 'R.Sharma', 'K.Rahul', 'V.Kohli', 'S.Yadav', 'R.Pant', 'H.Pandya'
        batsmen[6].name, batsmen[7].name, batsmen[8].name, batsmen[9].name, batsmen[10].name = 'R.Jadeja', 'S.Thakur', 'W.Sundar', 'B.Kumar','J.Bumrah'
        batsmen[0].kind, batsmen[1].kind, batsmen[2].kind, batsmen[3].kind, batsmen[4].kind, batsmen[5].kind = 1,1,1,1,0,1
        batsmen[6].kind, batsmen[7].kind, batsmen[8].kind, batsmen[9].kind, batsmen[10].kind = 0,1,0,1,1
        
    if play_choice == 'AUS':
        batsmen[0].name, batsmen[1].name, batsmen[2].name, batsmen[3].name, batsmen[4].name, batsmen[5].name = 'A.Finch', 'D.Warner', 'S.Smith', 'M.Labuschagne', 'G.Maxwell', 'M.Stoinis'
        batsmen[6].name, batsmen[7].name, batsmen[8].name, batsmen[9].name, batsmen[10].name = 'P.Cummins', 'N.Lyon', 'M.Starc', 'A.Zampa','J.Hzlwd'
        batsmen[0].kind, batsmen[1].kind, batsmen[2].kind, batsmen[3].kind, batsmen[4].kind, batsmen[5].kind = 1,0,1,1,1,1
        batsmen[6].kind, batsmen[7].kind, batsmen[8].kind, batsmen[9].kind, batsmen[10].kind = 1,1,0,1,0
        
    if play_choice == 'ENG':
        batsmen[0].name, batsmen[1].name, batsmen[2].name, batsmen[3].name, batsmen[4].name, batsmen[5].name = 'J.Roy', 'J.Buttler', 'D.Malan', 'J.Bairstow', 'B.Stokes', 'E.Morgan'
        batsmen[6].name, batsmen[7].name, batsmen[8].name, batsmen[9].name, batsmen[10].name = 'S.Curran', 'A.Rashid', 'J.Archer', 'C.Jordan','M.Wood'
        batsmen[0].kind, batsmen[1].kind, batsmen[2].kind, batsmen[3].kind, batsmen[4].kind, batsmen[5].kind = 1,1,0,1,0,0
        batsmen[6].kind, batsmen[7].kind, batsmen[8].kind, batsmen[9].kind, batsmen[10].kind = 0,1,1,1,1
        
    if play_choice == 'PAK':
        batsmen[0].name, batsmen[1].name, batsmen[2].name, batsmen[3].name, batsmen[4].name, batsmen[5].name = 'B.Azam', 'M.Rizwan', 'Hai.Ali', 'M.Hafeez', 'F.Ashraf', 'I.Wasim'
        batsmen[6].name, batsmen[7].name, batsmen[8].name, batsmen[9].name, batsmen[10].name = 'M.Nawaz', 'S.Khan', 'Has.Ali', 'H.Rauf','S.Afridi'
        batsmen[0].kind, batsmen[1].kind, batsmen[2].kind, batsmen[3].kind, batsmen[4].kind, batsmen[5].kind = 1,1,1,1,0,0
        batsmen[6].kind, batsmen[7].kind, batsmen[8].kind, batsmen[9].kind, batsmen[10].kind = 0,1,1,1,0

    if opp_choice == 'IND':
        bowlers[0].name, bowlers[1].name, bowlers[2].name, bowlers[3].name, bowlers[4].name = 'W.Sundar','B.Kumar','J.Bumrah','R.Jadeja','S.Thakur'
        bowlers[0].x, bowlers[0].y, bowlers[0].x_or, bowlers[0].y_or, bowlers[0].x0, bowlers[0].y0, bowlers[0].kind, bowlers[0].hand = 363, 500, 363, 500,444, 412, 2, 1
        bowlers[1].x, bowlers[1].y, bowlers[1].x_or, bowlers[1].y_or, bowlers[1].x0, bowlers[1].y0, bowlers[1].kind, bowlers[1].hand = 363, 573, 363, 573,444, 412, 0, 1
        bowlers[2].x, bowlers[2].y, bowlers[2].x_or, bowlers[2].y_or, bowlers[2].x0, bowlers[2].y0, bowlers[2].kind, bowlers[2].hand = 363, 573, 363, 573,444, 412, 1, 1
        bowlers[3].x, bowlers[3].y, bowlers[3].x_or, bowlers[3].y_or, bowlers[3].x0, bowlers[3].y0, bowlers[3].kind, bowlers[3].hand = 363, 500, 363, 500,444, 412, 3, 0
        bowlers[4].x, bowlers[4].y, bowlers[4].x_or, bowlers[4].y_or, bowlers[4].x0, bowlers[4].y0, bowlers[4].kind, bowlers[4].hand = 363, 573, 363, 573,444, 412, 0, 1
        
    if opp_choice == 'AUS':
        bowlers[0].name, bowlers[1].name, bowlers[2].name, bowlers[3].name, bowlers[4].name = 'J.Hzlwood','P.Cummins','M.Starc','N.Lyon','A.Zampa'
        bowlers[0].x, bowlers[0].y, bowlers[0].x_or, bowlers[0].y_or, bowlers[0].x0, bowlers[0].y0, bowlers[0].kind, bowlers[0].hand = 363, 573, 363, 573,444, 412, 0, 1
        bowlers[1].x, bowlers[1].y, bowlers[1].x_or, bowlers[1].y_or, bowlers[1].x0, bowlers[1].y0, bowlers[1].kind, bowlers[1].hand = 363, 573, 363, 573,444, 412, 1, 1
        bowlers[2].x, bowlers[2].y, bowlers[2].x_or, bowlers[2].y_or, bowlers[2].x0, bowlers[2].y0, bowlers[2].kind, bowlers[2].hand = 580, 573, 580, 573,580, 412, 1, 0
        bowlers[3].x, bowlers[3].y, bowlers[3].x_or, bowlers[3].y_or, bowlers[3].x0, bowlers[3].y0, bowlers[3].kind, bowlers[3].hand = 363, 500, 363, 500,444, 412, 2, 1
        bowlers[4].x, bowlers[4].y, bowlers[4].x_or, bowlers[4].y_or, bowlers[4].x0, bowlers[4].y0, bowlers[4].kind, bowlers[4].hand = 363, 500, 363, 500,444, 412, 3, 1
        
    if opp_choice == 'ENG':
        bowlers[0].name, bowlers[1].name, bowlers[2].name, bowlers[3].name, bowlers[4].name = 'M.Wood','J.Archer','C.Jordan','A.Rashid','B.Stokes'
        bowlers[0].x, bowlers[0].y, bowlers[0].x_or, bowlers[0].y_or, bowlers[0].x0, bowlers[0].y0, bowlers[0].kind, bowlers[0].hand = 363, 573, 363, 573,444, 412, 1, 1
        bowlers[1].x, bowlers[1].y, bowlers[1].x_or, bowlers[1].y_or, bowlers[1].x0, bowlers[1].y0, bowlers[1].kind, bowlers[1].hand = 363, 573, 363, 573,444, 412, 0, 1
        bowlers[2].x, bowlers[2].y, bowlers[2].x_or, bowlers[2].y_or, bowlers[2].x0, bowlers[2].y0, bowlers[2].kind, bowlers[2].hand = 363, 573, 363, 573,444, 412, 1, 1
        bowlers[3].x, bowlers[3].y, bowlers[3].x_or, bowlers[3].y_or, bowlers[3].x0, bowlers[3].y0, bowlers[3].kind, bowlers[3].hand = 363, 500, 363, 500,444, 412, 3, 1
        bowlers[4].x, bowlers[4].y, bowlers[4].x_or, bowlers[4].y_or, bowlers[4].x0, bowlers[4].y0, bowlers[4].kind, bowlers[4].hand = 363, 573, 363, 573,444, 412, 0, 1
        
    if opp_choice == 'PAK':
        bowlers[0].name, bowlers[1].name, bowlers[2].name, bowlers[3].name, bowlers[4].name = 'S.Afridi','H.Rauf','H.Ali','M.Nawaz','S.Khan'
        bowlers[0].x, bowlers[0].y, bowlers[0].x_or, bowlers[0].y_or, bowlers[0].x0, bowlers[0].y0, bowlers[0].kind, bowlers[0].hand = 580, 573, 580, 573,580, 412, 1, 0
        bowlers[1].x, bowlers[1].y, bowlers[1].x_or, bowlers[1].y_or, bowlers[1].x0, bowlers[1].y0, bowlers[1].kind, bowlers[1].hand = 363, 573, 363, 573,444, 412, 0, 1
        bowlers[2].x, bowlers[2].y, bowlers[2].x_or, bowlers[2].y_or, bowlers[2].x0, bowlers[2].y0, bowlers[2].kind, bowlers[2].hand = 363, 573, 363, 573,444, 412, 1, 1
        bowlers[3].x, bowlers[3].y, bowlers[3].x_or, bowlers[3].y_or, bowlers[3].x0, bowlers[3].y0, bowlers[3].kind, bowlers[3].hand = 363, 500, 363, 500,444, 412, 3, 0
        bowlers[4].x, bowlers[4].y, bowlers[4].x_or, bowlers[4].y_or, bowlers[4].x0, bowlers[4].y0, bowlers[4].kind, bowlers[4].hand = 363, 500, 363, 500,444, 412, 3, 1
        
    #re-initialization
    for man in batsmen:
        man.hit, man.wrong, man.shot, man.runs, man.balls = False, False, 0, 0, 0
    for man in bowlers:
        man.count, man.run, man.hasrun, man.delivered, man.runs, man.wickets, man.balls = 0, False, False, False, 0,0,0
    cherry.x0, cherry.y0, cherry.x1, cherry.y1, cherry.x2, cherry.y2, cherry.xchange1, cherry.xchange2 = 0,0,0,0,0,0,0,0
    cherry.x, cherry.y, cherry.generated, cherry.hit, cherry.vector, cherry.vmag = 0,0,False, False, (0,0), 0  
    
    play = True
    lose = False
    win = False
    tie = False

    global score
    score = 0
    global wickets
    wickets = 0
    global balls
    balls = 0
    target = int(250 + (300 - 250)*np.random.random())

    global action
    action = -1

    global prev_stri  #previous ball
    global prev_nonstri
    global stri  #upcoming ball
    global nonstri

    prev_stri, prev_nonstri, stri, nonstri = 0, 1, 0, 1 #before the gameloop has begun, top 2 batsmen take strike! #these get updated as the game proceeds
                                                                                            
    while play:
        if lose or win or tie:
            screen.blit(match_end, (0,0))
            text_screen(score_font, 'Press H for Home', black, 20, 50)
             
            screen.blit(match_end_bat, (225, 235))
            text_screen(event_font, str(score)+'/'+str(wickets) + '(' + str(balls//6) +'.' +str(balls%6) +')', black, 700, 350 )
            y_bat = 4
            for i in range(0,11):
                text_screen(score_font, batsmen[i].name, white, 225 + 5, 235 + y_bat)
                text_screen(score_font,  str(batsmen[i].runs) + '(' + str(batsmen[i].balls) +')', white, 225 + 240, 235 + y_bat)
                y_bat = y_bat + 40
            

            
            screen.blit(match_end_bowl, (810, 465))
            y_bowl = 4
            for i in range(0,5):
                text_screen(score_font, bowlers[i].name, white, 810 + 5, 465 + y_bowl)
                text_screen(score_font, str(bowlers[i].wickets)+ '-'+str(bowlers[i].runs) + '(' + str(bowlers[i].balls//6) +'.' +str(bowlers[i].balls%6) +')', white, 810 + 195, 465 + y_bowl)
                y_bowl = y_bowl + 40
            
            
            if lose:
                text_screen(event_font, opp_choice+' Win By '+str(target - 1 - score)+' runs', black, screen_width*0.05, screen_height*0.10)
            if win:
                text_screen(event_font,play_choice+' Win By '+ str(10-wickets)+' wickets', black, screen_width*0.10, screen_height*0.10)
            if tie:
                text_screen(event_font,'Match Tied', black, screen_width*0.05, screen_height*0.10)
    
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        homescreen()
                    
        else:
            selected_bowler = select_bowler(bowlers, balls)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    play = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        homescreen()
                    if event.key == pygame.K_SPACE:
                        if not selected_bowler.hasrun:
                            selected_bowler.run = True
                            selected_bowler.hasrun = True
                        cherry.generate_ball(selected_bowler, batsmen[stri])
                    
                    if selected_bowler.delivered: #only hit after ball is delivered
                        if not batsmen[stri].hit:   #once you hit, cant hit again. This is necessary to make scoring possible based on one shot selected...
                        
                            if event.key == pygame.K_LEFT:
                                if 218<= cherry.y1 <=266.5:
                                    cherry.vector = (-0.707,0.707)
                                    batsmen[stri].shot = 2
                                    batsmen[stri].hit = True
                                        
                                if 266.5<cherry.y1:
                                    cherry.vector = (-1,0)
                                    batsmen[stri].shot = 1
                                    batsmen[stri].hit = True
                                
                                if batsmen[stri].kind == 1:    
                                    if cherry.x2>580:
                                        batsmen[stri].wrong = True
                                        action = 7
                                if batsmen[stri].kind == 0:    
                                    if cherry.x2>610:
                                        batsmen[stri].wrong = True
                                        action = 7
   
                            if event.key == pygame.K_DOWN:  
                                cherry.vector = (0,1)
                                batsmen[stri].shot = 3
                                batsmen[stri].hit = True

                                if batsmen[stri].kind == 1:
                                    if cherry.y1>266.5 or cherry.x2<500 or cherry.x2>580:
                                        batsmen[stri].wrong = True
                                        action = 7
                                if batsmen[stri].kind == 0: 
                                    if cherry.y1>266.5 or cherry.x2<525 or cherry.x2>610:
                                        batsmen[stri].wrong = True
                                        action = 7


                            if event.key == pygame.K_RIGHT:
                                if 218<= cherry.y1 <=266.5:
                                    cherry.vector = (0.707,0.707)
                                    batsmen[stri].shot = 5
                                    batsmen[stri].hit = True
                                        
                                if 266.5< cherry.y1:
                                    cherry.vector = (1,0)
                                    batsmen[stri].shot = 4
                                    batsmen[stri].hit = True

                                if batsmen[stri].kind == 1:
                                    if cherry.x2<500:
                                        batsmen[stri].wrong = True
                                        action = 7
                                if batsmen[stri].kind == 0:
                                    if cherry.x2<525:
                                        batsmen[stri].wrong = True
                                        action = 7

                            scoring(selected_bowler, batsmen[stri]) #scoring only considered at the moment of contact and if the batsman doesnt play a wrong or does offer a shot
                                
                                    
            if not selected_bowler.delivered: #return to stance after ball is back to bowler
                batsmen[stri].shot = 0
               
            if selected_bowler.delivered and not batsmen[stri].hit: #doesnt trigger in event loop, so doing separately
                action = 7
                        
            screen.blit(ground, (0,0))
            text_screen(score_font, 'Press H for Home', black, 20 , 50)
            text_screen(score_font, 'Press SpcBar to Bowl', black, 20, 70)
            text_screen(score_font, 'Press Arrow Keys to Hit', black, 20, 90)
            
            screen.blit(logo, (1000, 0))
            selected_bowler.move_and_draw()
            draw_runner(selected_bowler)
            wk.draw(selected_bowler, cherry)
            batsmen[stri].draw()
            
            cherry.deliver_ball(selected_bowler, batsmen[stri])
            cherry.hit_ball(selected_bowler, batsmen[stri])
            cherry.lbw_bowled(selected_bowler, batsmen[stri])
            ump.draw(action)
        
            #left_panel
            screen.blit(left_panel, (40, 550))
            text_screen(score_font, play_choice, black, 40 + 3, 550 + 3)
            
            text_screen(score_font, str(score)+'/'+str(wickets) + '(' + str(balls//6) +'.' +str(balls%6) +')', white, 40 + 50, 550 + 8)
            text_screen(score_font, str(target), white, 40 + 200, 550 + 8)
            
            text_screen(score_font, batsmen[stri].name, white, 42, 550 + 41)
            text_screen(score_font,  str(batsmen[stri].runs) + '(' + str(batsmen[stri].balls) +')', white, 40 + 175, 550 + 41)
            
            text_screen(score_font, batsmen[nonstri].name, white, 42, 550 + 80)
            text_screen(score_font,  str(batsmen[nonstri].runs) + '(' + str(batsmen[nonstri].balls) +')', white, 40 + 175, 550 + 80)

            text_screen(score_font, selected_bowler.name, white, 42, 550 + 113)
            text_screen(score_font, str(selected_bowler.wickets)+ '-'+str(selected_bowler.runs) + '(' + str(selected_bowler.balls//6) +'.' +str(selected_bowler.balls%6) +')', white, 40 + 160, 550 + 113)

            #right_panel
            screen.blit(right_panel, (880, 550))
            if balls ==0:
                text_screen(score_font, 'CurrRR: 0', white, 882, 550 + 12)
            else:
                text_screen(score_font, 'CurrRR: '+ str("%.2f"%(score/(balls/6))), white, 882, 550 + 12)
            if balls == 120:
                text_screen(score_font, 'ReqRR: Infinity', white, 882, 550 + 12)
            else:
                text_screen(score_font, 'ReqRR: '+str("%.2f"%((target-score)/((120-balls)/6))), white, 880 + 162, 550 + 12)
            text_screen(score_font, 'Need ' + str(target - score) + ' runs from ' + str(120 - balls)+' balls', white, 882, 550 + 82)
            

            

            show_event(cherry, balls)
           

            if (wickets == 10 and score<target-1):
                lose = True

            if (balls == 120 and score<target-1):
                if 0<= action<=6 and (cherry.x<0 or cherry.x>screen_width or cherry.y<0 or cherry.y> screen_height):
                    lose = True
                if action == 7 and cherry.y<cherry.y2:
                    lose = True
                    

            if score>= target and (cherry.x<0 or cherry.x>screen_width or cherry.y<0 or cherry.y> screen_height):
                win = True
                

            if score == target -1  and (balls == 120 or wickets == 10):
                tie = True
                
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

homescreen()



    
   
