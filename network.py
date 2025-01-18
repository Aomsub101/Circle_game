"""
์Networking file.
Handling data traffic from client

Compose with
1. importing game_engine to calculate data from client
2. Have Client class for needed client data
3. have handle_client_data func.
4. have init_server function for initilize connection
"""

import socket
import threading
import sys
import random as r
import fake_game_engine
# import game_engine

HOST = '0.0.0.0'
PORT = 12345 # server port

# Window constant
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

clients = [] # list of clients
players = []
food_list = []

class Client:
    """
    Client class.
    """
    def __init__(self, client_socket, client_id):
        self.client_socket = client_socket
        self.client_id = client_id

class Player:
    """
    Player class
    """
    def __init__(self, name, player_id):
        self.id = player_id
        self.name = name
        self.dir = r.randint(0, 360)
        self.color = (r.randint(0,255), r.randint(0,255), r.randint(0,255))
        self.radius = 8
        self.x = r.randint(self.radius, SCREEN_WIDTH-self.radius)
        self.y = r.randint(self.radius, SCREEN_HEIGHT-self.radius)
        self.speed = 0
        self.score = 0

class Food:
    """
    Food class
    """
    def __init__(self):
        self.color = (r.randint(0,255), r.randint(0,255), r.randint(0,255))
        self.radius = r.randint(3,5)
        self.x = r.randint(50,SCREEN_WIDTH-50)
        self.y = r.randint(50,SCREEN_HEIGHT-50)

def food_generator():
    """
    generating food
    """
    while len(food_list) != 50:
        food = Food()
        food_list.append(food)

def translate_data():
    """
    turn an object data into message
    """
    message = ""
    for player in players:
        for data in list(player.__dict__.values()):
            message += data + ','
        message = message[:-1] + ';'

    message = message[:-1] + "/"

    for food in food_list:
        for data in list(food.__dict__.values()):
            message += data + ','
        message = message[:-1] + ';'

    message = message[:-1]

    return message

def broad_data_to_clients():
    """
    Sending back data to all the clients client
    """
    message = translate_data()
    for client in clients:
        client.client_socket.send(message.encode())

def handle_game_state(client, key):
    """
    Use game_engine
    Update position, etc
    """
    if len(food_list) != 50:
        food_generator()

    players[client.client_id] = fake_game_engine.calculate(players[client.client_id], key)

    broad_data_to_clients()


def create_player(cli, conn):
    """
    Creating player for client
    """
    name = ""
    cli.client_socket.send("Enter your name: ").encode()
    while True:
        name_chunk = conn.recv(1024).decode()
        if name_chunk:
            if name_chunk == "\n":
                break
            name += name_chunk
        else:
            break
    player = Player(name, cli.client_id)
    players.append(player)


def handle_key(client, conn):
    """
    For recieve data from client (every player's properties)
    
    Data can be calculate inside here. (Maybe)
    """

    while True:
        # wait for a data from client
        key = ""
        while True:
            data = conn.recv(1024).decode()
            if data:
                # if data == "\n":
                #     break
                key += data
            else:
                break

        if key:
            handle_game_state(client, key)


def init_server():
    """
    Initialize server socket and open for connection
    """
    # creating server socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
    except OSError as msg:
        server_socket = None
        print(f'Error creating socket: {msg}')
        sys.exit(1)

    # binding and open for connection
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('Waiting for connection...')
    except OSError as msg:
        print('Error binding/listening!: ', msg)
        server_socket.close()
        sys.exit(1)

    while True:
        conn, address = server_socket.accept()
        print(f"Client: {address} join the room.")
        cli = Client(conn, len(clients))
        clients.append(cli)
        cli_thread = threading.Thread(target=handle_key,args=(cli, conn))
        cli_thread.start()
        create_player(cli, conn)

init_server()

# End of file
