import math
import random

# Constants for the game engine
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
THRUST = 0.5
TURN_ANGLE = 5  # degrees
FRICTION = 0.98  # slows down the player slightly
FPS = 60

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.angle = 0  # in degrees
        self.speed_x = 0
        self.speed_y = 0
        self.color = color

    def update_position(self, input_data):
        if 'w' in input_data:
            # Apply thrust in the direction of the current angle
            rad = math.radians(self.angle)
            self.speed_x += math.cos(rad) * THRUST
            self.speed_y += math.sin(rad) * THRUST

        if 'a' in input_data:
            # Turn left
            self.angle -= TURN_ANGLE

        if 'd' in input_data:
            # Turn right
            self.angle += TURN_ANGLE

        # Update position with current speed
        self.x += self.speed_x
        self.y += self.speed_y

        # Apply friction to gradually reduce speed
        self.speed_x *= FRICTION
        self.speed_y *= FRICTION

        # Keep the player within screen bounds
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

class Food:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

    def respawn(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

def main():
    # Initialize players and food
    player1 = Player(100, 100, "red")
    player2 = Player(700, 500, "blue")
    food = Food()

    # Simulate game loop
    frame_count = 0
    while True:
        frame_count += 1

        # Mock input for both players (example, random for demo purposes)
        input_player1 = random.choice([[], ['w'], ['a'], ['d'], ['w', 'a'], ['w', 'd']])
        input_player2 = random.choice([[], ['w'], ['a'], ['d'], ['w', 'a'], ['w', 'd']])

        # Update player positions
        player1.update_position(input_player1)
        player2.update_position(input_player2)

        # Print positions every 10 frames
        if frame_count % 10 == 0:
            print(f"Frame {frame_count}:")
            print(f"Player 1 - X: {player1.x:.2f}, Y: {player1.y:.2f}, Angle: {player1.angle}")
            print(f"Player 2 - X: {player2.x:.2f}, Y: {player2.y:.2f}, Angle: {player2.angle}")
            print(f"Food - X: {food.x}, Y: {food.y}")
            print("-" * 30)

        # Add a condition to stop the loop (for example, after 100 frames)
        if frame_count >= 100:
            break

if __name__ == "__main__":
    main()