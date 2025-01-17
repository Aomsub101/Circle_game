import pygame
import math
import random
import time

pygame.init()

# ------- Constants ---------

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 200, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
AQUA = (0, 255, 255)

# Sceen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAPTION = "EAT THE DOT"
FPS = 60

# Player
MAX_SPEED = 5
ACCELERATION = 0.2
DECELERATION = 0.05
TURN_SPEED = 0.08

# --------------------------

# setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)
clocks = pygame.time.Clock()
running = True  

class MockPlayer():
    def __init__(self, name, x, y, direction, color, radius, forward_key, turn_left_key, turn_right_key):
        self.name = name
        self.x = x
        self.y = y
        self.dir = direction
        self.color = color
        self.radius = radius
        self.speed = 0
        self.score = 0
        self.forward_key = forward_key
        self.turn_left_key = turn_left_key
        self.turn_right_key = turn_right_key
        
    def update(self):
        self.x += math.cos(self.dir) * self.speed
        self.y -= math.sin(self.dir) * self.speed
        if self.x <= 0:
            self.x = SCREEN_WIDTH - 1
        elif self.x >= SCREEN_WIDTH - 1:
            self.x = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT - 1
        elif self.y >= SCREEN_HEIGHT - 1:
            self.y = 0
            
        self.speed-=DECELERATION
        self.speed = max(self.speed,0)
        self.speed = min(self.speed,MAX_SPEED)
        
            
    def accelerate_and_turn(self, Key):
        if Key[self.turn_right_key]:
            self.dir -= TURN_SPEED
        elif Key[self.turn_left_key]:
            self.dir += TURN_SPEED
        if Key[self.forward_key]:
            self.speed += ACCELERATION
        
        if self.dir >= 2*math.pi:
            self.dir -= 2*math.pi
        elif self.dir < 0:
            self.dir += 2*math.pi
            
    def check_collision(self, food):
        distance = math.sqrt((self.x-food.x)**2 + (self.y-food.y)**2)
        if distance <= food.radius + self.radius:
            return True
        return False
    
    def check_player_eatable(self, player):
        distance = math.sqrt((self.x-player.x)**2 + (self.y-player.y)**2)
        if distance <= self.radius-player.radius and self.radius-player.radius >= 3:
            return True
        return False
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, ((self.x+self.radius*0.5*math.cos(self.dir), self.y-self.radius*0.5*math.sin(self.dir))), self.radius//3)
        



class MockFood():
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def mock_food_generator(food_list):
    food = MockFood(random.randint(50, SCREEN_WIDTH),random.randint(50, SCREEN_HEIGHT), random.choice([RED,GREEN,BLUE,YELLOW,PURPLE,AQUA]), 5)
    food_list.append(food)


player1 = MockPlayer("Jedi", random.randint(50, SCREEN_WIDTH),
                     random.randint(50, SCREEN_HEIGHT),
                     1.5*math.pi, RED, 8, pygame.K_w, pygame.K_a, pygame.K_d)
player2 = MockPlayer("Aomsub",random.randint(50, SCREEN_WIDTH),
                     random.randint(50, SCREEN_HEIGHT),
                     1.5*math.pi, GREEN, 8, pygame.K_t, pygame.K_f, pygame.K_h)
player3 = MockPlayer(r"Champ",random.randint(50, SCREEN_WIDTH),
                     random.randint(50, SCREEN_HEIGHT),
                     1.5*math.pi, BLUE, 8, pygame.K_i, pygame.K_j, pygame.K_l)

food_list = []

player_list = [
    player1,
    player2,
    player3
]

def update_score_board(player_list):
    font = pygame.font.Font(None, 32)
    header_text = "Scoreboard"
    header = font.render(header_text, True, WHITE)
    screen.blit(header, (10, 10))
    player_list.sort(reverse=True, key=lambda x: x.score)
    for i,player in enumerate(player_list):
        score_text = f"{i+1}. {player.name} : {player.score}"
        score_board = font.render(score_text, True, player.color)
        screen.blit(score_board, (10, 15+25*(i+1)))
    
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # ------------ simulate engine -----------
    keys = pygame.key.get_pressed()
    
    if len(food_list) != 50:
        mock_food_generator(food_list)
    # ----------------------------------------
    
    for food in food_list:
        food.draw() # grafics function
        # ------------ simulate engine -----------
        for player in player_list:
            if player.check_collision(food):
                food_list.remove(food)
                mock_food_generator(food_list)
                player.score += 1
                player.radius += 0.5
        # ----------------------------------------
    player_list.sort(key=lambda x: x.score)
    for player in player_list:
        # ------------ simulate engine -----------
        for other_player in player_list:
            if player.check_player_eatable(other_player):
                player_list.remove(other_player)
            
        # ------------------------------------
        player.accelerate_and_turn(keys)
        player.update()
        # ----------------------------------------
        player.draw() # graphics function
    player_list.sort(reverse=True, key=lambda x: x.score)
        
    update_score_board(player_list) # graphics function
    
    pygame.display.flip()
    
    clocks.tick(FPS)