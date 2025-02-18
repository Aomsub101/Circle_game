import socket
import threading
import sys
import time
from game_engine import Player, Food, FOOD_COUNT, parse_keys, generate_state_string, GOAL_SCORE

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

rotating_handler = RotatingFileHandler(
    filename = 'log/server_logs.log',
    maxBytes=1024*1024,
    backupCount=5,
)

rotating_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(rotating_handler)

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

UPDATE_RATE = 1/60  # 60 FPS

class GameServer:
    def __init__(self):
        self.clients = {}  # client_id -> socket
        self.players = {}  # client_id -> Player
        self.address = {} # client_socket -> address
        self.foods = []
        self.running = True
        self.lock = threading.Lock()  # For thread-safe state updates

    def start(self):
        """Initialize and start the game server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()
            # Add log here +++++++++++++++++++++++++
            print(f"Server started on port {PORT}")
            logger.info("Server listenning or port: %s", PORT)

            update_thread = threading.Thread(target=self.update_loop)
            update_thread.start()

            while self.running:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                logger.info('Player %s connected', address)
                # Start client handler thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()

        except Exception as e:
            print(f"Server error: {e}")
            self.cleanup()

    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        try:
            name_data = client_socket.recv(1024).decode().strip()
            logger.info('Data received from %s: %s', address, name_data)
            if not name_data:
                return

            with self.lock:
                client_id = len(self.clients)
                self.clients[client_id] = client_socket
                self.players[client_id] = Player(name_data, client_id)
                self.address[client_socket] = address

            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    if data == b"RESET":
                        name_data = client_socket.recv(1024).decode().strip()
                        with self.lock:
                            old_won = self.players[client_id].won_last_match
                            self.players[client_id] = Player(name_data, client_id)
                            self.players[client_id].won_last_match = old_won
                        continue

                    with self.lock:
                        if client_id in self.players:
                            keys = parse_keys(data)
                            logger.info('Data recieved from %s: key %s',address, keys)
                            self.players[client_id].update(keys)

                except ConnectionError:
                    break

        except Exception as e:
            print(f"Client handler error: {e}")

        finally:
            # Cleanup disconnected client
            with self.lock:
                if client_id in self.clients:
                    del self.clients[client_id]
                if client_id in self.players:
                    del self.players[client_id]
            client_socket.close()
            print(f"Client {address} disconnected", address)
            logger.info("Player %s disconnected due to bad skilled play.", address)

    def update_loop(self):
        """Main game update loop"""
        while self.running:
            start_time = time.time()

            with self.lock:
                while len(self.foods) < FOOD_COUNT:
                    self.foods.append(Food())

                # Check collisions
                for player in list(self.players.values()):
                    # Food collisions
                    for food in list(self.foods):
                        if player.check_food_collision(food):
                            player.eat_food()
                            self.foods.remove(food)

                    # Player collisions
                    for other in list(self.players.values()):
                        if player.check_player_collision(other):
                            player.eat_player(other)
                            # Notify client of death
                            self.clients[other.client_id].send(b"DEAD")
                            # Remove eaten player
                            del self.players[other.client_id]

                    # Check win condition
                    if player.score >= GOAL_SCORE:
                        player.won_last_match = 1
                        for client_socket in self.clients.values():
                            client_socket.send(b"WINNER:" + player.name.encode())
                            # Add log here +++++++++++++++++++++++++
                            logger.info("Data sent to %s: WINNER: %s", self.address[client_socket], player.name)
                        self.players.clear()
                        self.foods.clear()
                        break

                # Broadcast game state
                state = generate_state_string(self.players.values(), self.foods)
                for client_socket in self.clients.values():
                    try:
                        client_socket.send(state.encode())
                        # Add log here +++++++++++++++++++++++++
                        logger.info("Data sent to %s: %s", self.address[client_socket],state)
                    except ConnectionError:
                        continue

            elapsed = time.time() - start_time
            if elapsed < UPDATE_RATE:
                time.sleep(UPDATE_RATE - elapsed)

    def cleanup(self):
        """Clean up server resources"""
        self.running = False
        for client_socket in self.clients.values():
            client_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server.cleanup()
