import math
import random

# ------- Constants ---------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player
MAX_SPEED = 4.5  # Slightly reduced for better control
ACCELERATION = 0.18
DECELERATION = 0.04
TURN_SPEED = 0.07
INITIAL_RADIUS = 8
RADIUS_GROWTH = 0.3  # Reduced for better balance
GOAL_SCORE = 200

# Food
FOOD_COUNT = 50
MIN_FOOD_SPAWN_DISTANCE = 50
FOOD_RADIUS = 5

# --------------------------

class Player:
    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.dir = random.random() * 2 * math.pi
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.radius = INITIAL_RADIUS
        self.speed = 0
        self.score = 0
        self.won_last_match = 0
        
    def update(self, keys):
        # Handle turning
        if 'd' in keys:
            self.dir -= TURN_SPEED
        if 'a' in keys:
            self.dir += TURN_SPEED
        
        # Handle acceleration
        if 'w' in keys:
            self.speed += ACCELERATION
        
        # Apply movement
        self.speed = max(0, min(self.speed - DECELERATION, MAX_SPEED))
        self.x += math.cos(self.dir) * self.speed
        self.y -= math.sin(self.dir) * self.speed
        
        # Wrap around screen
        self.x = self.x % SCREEN_WIDTH
        self.y = self.y % SCREEN_HEIGHT
        
    def check_food_collision(self, food):
        distance = math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)
        return distance <= self.radius + food.radius
    
    def check_player_collision(self, other):
        if self.client_id == other.client_id:
            return False
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return (distance <= self.radius and 
                self.radius > other.radius * 1.2)  # Must be 20% larger to eat
    
    def eat_food(self):
        self.score += 1
        self.radius += RADIUS_GROWTH
    
    def eat_player(self, other):
        self.score += int(other.score / 2)  # Get half the eaten player's score
        self.radius += other.radius / 3  # Get third of their size
        
    def to_string(self):
        color_str = ".".join(map(str, self.color))
        return f"{self.name},{self.x},{self.y},{self.dir},{color_str},{self.radius},{self.score},{self.won_last_match}"

class Food:
    def __init__(self):
        self.respawn()
        
    def respawn(self):
        self.x = random.randint(MIN_FOOD_SPAWN_DISTANCE, SCREEN_WIDTH - MIN_FOOD_SPAWN_DISTANCE)
        self.y = random.randint(MIN_FOOD_SPAWN_DISTANCE, SCREEN_HEIGHT - MIN_FOOD_SPAWN_DISTANCE)
        self.radius = FOOD_RADIUS
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def to_string(self):
        return f"{self.x},{self.y},{self.radius}"

def parse_keys(key_data):
    """Convert byte string of keys to list"""
    if not key_data:
        return []
    return key_data.decode('utf-8').split(',')

def generate_state_string(players, foods):
    """Generate network string from game state"""
    player_strings = [p.to_string() for p in players]
    food_strings = [f.to_string() for f in foods]
    return f"{';'.join(player_strings)}/{';'.join(food_strings)}"

def parse_state_string(state_string):
    """Parse network string into player and food data"""
    player_string, food_string = state_string.split('/')
    
    players_data = []
    if player_string:
        for p in player_string.split(';'):
            name, x, y, d, c, r, score, won = p.split(',')
            players_data.append({
                'name': name,
                'x': float(x),
                'y': float(y),
                'dir': float(d),
                'color': tuple(map(int, c.split('.'))),
                'radius': float(r),
                'score': int(score),
                'won_last_match': int(won)
            })
    
    foods_data = []
    if food_string:
        for f in food_string.split(';'):
            x, y, r = f.split(',')
            foods_data.append({
                'x': float(x),
                'y': float(y),
                'radius': float(r)
            })
            
    return players_data, foods_data