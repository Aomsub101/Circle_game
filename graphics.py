import pygame
import math
import random
import time

pygame.init()

# ------- Constants ---------

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    def __init__(self, x, y, direction, color, radius):
        self.x = x
        self.y = y
        self.dir = direction
        self.color = color
        self.radius = radius
        self.speed = 0
        
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
        if Key[pygame.K_d]:
            self.dir -= TURN_SPEED
        elif Key[pygame.K_a]:
            self.dir += TURN_SPEED
        if Key[pygame.K_w]:
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
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, self.color, (self.x,self.y), 
                                            (self.x+self.radius*2*math.cos(self.dir),
                                             self.y-self.radius*2*math.sin(self.dir)), self.radius//2)

class MockFood():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK
        self.radius = 10
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def mock_food_generator(food_list):
    food = MockFood(random.randint(50, SCREEN_WIDTH),random.randint(50, SCREEN_HEIGHT))
    food_list.append(food)


player1 = MockPlayer(100,100,1.5*math.pi, RED, 20)
player2 = MockPlayer(200,200,1.5*math.pi, GREEN, 20)
player3 = MockPlayer(300,300,1.5*math.pi, BLUE, 20)

food_list = []

player_list = [
    player1,
    player2,
    player3
]

score = 0

def show_score(score):
    font = pygame.font.Font(None, 32)
    text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(text, (10, 10))

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if not food_list:
        mock_food_generator(food_list)
    
    for food in food_list:
        food.draw()
        if player1.check_collision(food):
            food_list.remove(food)
            mock_food_generator(food_list)
            score += 1
            
    show_score(score)
    player1.accelerate_and_turn(keys)
    player1.update()
    player1.draw()
    
    pygame.display.flip()
    
    clocks.tick(FPS)