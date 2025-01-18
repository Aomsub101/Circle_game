import socket
import pygame
import threading
import sys
from graphics_engine import GraphicsEngine
from game_engine import parse_state_string

# ------- Constants ---------
SERVER_HOST = 'localhost'  # Change to server IP if running on different machine
SERVER_PORT = 12345

# Key mapping
CONTROL_KEYS = {pygame.K_w: 'w', 
                pygame.K_a: 'a', 
                pygame.K_d: 'd'}

UPDATE_RATE = 1/60  # 60 FPS
# --------------------------

class GameClient:
    def __init__(self):
        self.graphics = GraphicsEngine()
        self.running = True
        self.game_state = {'players': [], 'foods': []}
        self.lock = threading.Lock()  # For thread-safe state updates
        
    def connect_to_server(self):
        """Establish connection with game server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to server")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def start_game(self):
        """Main game loop"""
        while self.running:
            # Get player name
            name = self.graphics.get_name_input()
            if not name:  # User closed window
                break
                
            # Send name to server
            try:
                self.socket.send(name.encode())
            except ConnectionError:
                print("Lost connection to server")
                break
                
            # Start receiver thread
            receiver_thread = threading.Thread(target=self.receive_data)
            receiver_thread.start()
            
            # Main game loop
            self.game_loop()
            
            # If we're here, player died or game ended
            receiver_thread.join()
            
        self.cleanup()
        
    def game_loop(self):
        """Handle game inputs and rendering"""
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                    
            # Get pressed keys
            keys = pygame.key.get_pressed()
            pressed = []
            for key, value in CONTROL_KEYS.items():
                if keys[key]:
                    pressed.append(value)
                    
            # Send key data to server
            try:
                if pressed:
                    self.socket.send(','.join(pressed).encode())
            except ConnectionError:
                print("Lost connection to server")
                return
                
            # Render current game state
            with self.lock:
                self.graphics.draw_game_state(
                    self.game_state['players'],
                    self.game_state['foods']
                )
                
            clock.tick(60)
            
    def receive_data(self):
        """Handle incoming server data"""
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                    
                # Handle special messages
                if data.startswith(b"DEAD"):
                    break
                elif data.startswith(b"WINNER:"):
                    winner_name = data[7:].decode()
                    # Get new name for next game
                    name = self.graphics.get_name_input(victory=True, 
                                                      winner_name=winner_name)
                    if not name:  # User closed window
                        self.running = False
                        break
                    # Request respawn
                    self.socket.send(b"RESET")
                    self.socket.send(name.encode())
                    continue
                    
                # Parse normal game state
                try:
                    players, foods = parse_state_string(data.decode())
                    with self.lock:
                        self.game_state['players'] = players
                        self.game_state['foods'] = foods
                except Exception as e:
                    print(f"Error parsing game state: {e}")
                    continue
                    
            except ConnectionError:
                print("Lost connection to server")
                break
                
        self.running = False
        
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        self.socket.close()
        self.graphics.cleanup()

if __name__ == "__main__":
    client = GameClient()
    if client.connect_to_server():
        client.start_game()