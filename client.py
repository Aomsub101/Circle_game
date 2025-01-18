import socket
import pygame
import threading
import sys
from graphics_engine import GraphicsEngine
from game_engine import parse_state_string

# ------- Constants ---------
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Key mapping
CONTROL_KEYS = {pygame.K_w: 'w', 
                pygame.K_a: 'a', 
                pygame.K_d: 'd'}

UPDATE_RATE = 1/60
# --------------------------

class GameClient:
    def __init__(self):
        self.graphics = GraphicsEngine()
        self.running = True
        self.game_state = {'players': [], 'foods': []}
        self.lock = threading.Lock()
        
    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to server")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def start_game(self):
        while self.running:
            name = self.graphics.get_name_input()
            if not name:
                break
                
            try:
                self.socket.send(name.encode())
            except ConnectionError:
                print("Lost connection to server")
                break
                
            receiver_thread = threading.Thread(target=self.receive_data)
            receiver_thread.start()
            
            self.game_loop()
            
            receiver_thread.join()
            
        self.cleanup()
        
    def game_loop(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                    
            keys = pygame.key.get_pressed()
            pressed = []
            for key, value in CONTROL_KEYS.items():
                if keys[key]:
                    pressed.append(value)
                    
            try:
                if pressed:
                    self.socket.send(','.join(pressed).encode())
            except ConnectionError:
                print("Lost connection to server")
                return
                
            with self.lock:
                self.graphics.draw_game_state(
                    self.game_state['players'],
                    self.game_state['foods']
                )
                
            clock.tick(60)
            
    def receive_data(self):
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                    
                if data.startswith(b"DEAD"):
                    break
                elif data.startswith(b"WINNER:"):
                    winner_name = data[7:].decode()
                    name = self.graphics.get_name_input(victory=True, 
                                                      winner_name=winner_name)
                    if not name:
                        self.running = False
                        break
                    
                    self.socket.send(b"RESET")
                    self.socket.send(name.encode())
                    continue
                    
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
        self.running = False
        self.socket.close()
        self.graphics.cleanup()

if __name__ == "__main__":
    client = GameClient()
    if client.connect_to_server():
        client.start_game()