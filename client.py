import socket
import pygame
import threading
import sys
from graphics_engine import Graphics

class Client:
    def __init__(self):
        self.graphics = Graphics()
        self.running = True
        self.players = []
        self.foods = []
        self.host = "172.20.10.5"
        self.port = 1090
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            return True
        except:
            print(f"Couldn't connect to {self.host}:{self.port}")
            return False
            
    def receive_data(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                    
                if data.startswith('win:'):
                    print(f"{data[4:]} won the game!")
                    self.running = False
                    break
                    
                # Parse game state
                players_part, foods_part = data.split('/')
                
                self.players = [p.split(',') for p in players_part.split(';')] if players_part else []
                self.foods = [f.split(',') for f in foods_part.split(';')] if foods_part else []
                
            except:
                break
                
        self.running = False
        
    def run(self):
        # Get player name
        name = self.graphics.get_name()
        if not name:
            return
            
        # Send name to server
        self.sock.send(name.encode())
        
        # Start receiver thread
        thread = threading.Thread(target=self.receive_data)
        thread.daemon = True
        thread.start()
        
        # Main game loop
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                    
            # Send input
            keys = pygame.key.get_pressed()
            pressed = []
            if keys[pygame.K_w]: pressed.append('w')
            if keys[pygame.K_a]: pressed.append('a')
            if keys[pygame.K_d]: pressed.append('d')
            
            if pressed:
                try:
                    self.sock.send(','.join(pressed).encode())
                except:
                    self.running = False
                    break
                    
            # Draw game state
            self.graphics.draw_game(self.players, self.foods)
            clock.tick(60)
            
        self.sock.close()
        self.graphics.cleanup()

if __name__ == "__main__":
    client = Client()
    if client.connect():
        client.run()