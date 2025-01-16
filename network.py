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
import random as r
# import game_engine

HOST = '0.0.0.0' # server IP
PORT = 12345 # server port

# Window constant
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

clients = [] # list of clients

class Client:
    """
    Class client. Compose with
        1. init - for handling client simple data.
    """
    def __init__(self, client_socket, client_id):
        self.client_socket = client_socket
        self.client_id = client_id
        self.x = r.randint() # Add range
        self.y = r.randint() # Add range
        self.radius = 10 # Change radius
        self.vx = 1 # change speed
        self.vy = 1 # change speed

def send_data_to_client(client, graphic_object):
    """
    Sending back data to client
    """
    client.send(graphic_object)

def handle_client_data(client, ):
    """
    For recieve data from client (w,a,d)
    Data can be calculate inside here. (Maybe)
    """

    # game_engine.calculate(some_data)
    # send_data_to_client(client, some_graphic_data)

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
        exit(1)

    # binding and open for connection
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('Waiting for connection...')
    except OSError as msg:
        print('Error binding/listening!')
        server_socket.close()
        exit(1)

    while True:
        connection, address = server_socket.accept()
        print(f"Client: {address} join the room.")
        cli = Client(connection, len(clients))
        clients.append(cli)
        cli_thread = threading.Thread(target=handle_client_data,args=(cli,))
        cli_thread.start()

init_server()