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

HOST = '0.0.0.0' # server IP
PORT = 12345 # server port

# Window constant
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600

clients = [] # list of clients

class Client:
    """
    Client class.
    """
    def __init__(self, client_socket, client_id):
        self.client_socket = client_socket
        self.client_id = client_id

player = {
    "name": "",
    "age": ""
}
obj_props = ["name", "age"]

def msg_to_obj_translator(message):
    """
    For translating message to obj.
    """
    data_list = message.split('/')
    for i in range(len(obj_props)):
        player[obj_props[i]] = data_list[i]
    
    print(player)

def obj_to_msg_translator(obj):
    """
    For translating object to message
    """
    message = ""
    for value in obj.values():
        message += value + '/'
    
    print(obj_to_msg_translator)

def send_data_to_client(graphic_object):
    """
    Sending back data to all the clients client
    """
    for client in clients:
        client.send(graphic_object)

def handle_client_data(client, conn):
    """
    For recieve data from client (every player's properties)
    
    Data can be calculate inside here. (Maybe)
    """

    # game_engine.calculate(some_data)
    # send_data_to_client(client, some_graphic_data)

    while True:
        # wait for a data from client
        message = ""
        while True:
            data = conn.recv(1024).decode()
            if data:
                if data == "\n":
                    break
                message += data
            else:
                break

        if message:
            msg_to_obj_translator(message)
            # fake_game_engine.calculate(some_obj) # whatever this is
        else:
            break

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
        cli_thread = threading.Thread(target=handle_client_data,args=(cli, conn))
        cli_thread.start()

init_server()

# End of file
