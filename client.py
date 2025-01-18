"""
Client file.
For testing and real use in game.
"""

import socket
import threading
import graphic

HOST = "127.0.0.1" # server IP
PORT = 12345 # server port

obj_props = ['name', 'age']

class Player():
    """
    Player class
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age

def msg_to_obj_translator(message, player):
    """
    For translating message to obj.
    """
    data_list = message.split('/')
    for i in range(len(obj_props)):
        setattr(player, obj_props[i], data_list[i])

def obj_to_msg_translator(player):
    """
    For translating object to message
    """
    message = ""
    for value in list(player.__dict__.values()):
        message += str(value) + '/'

    return message

def send_player_data(client, player):
    """
    Sending player's data to server
    """
    message = obj_to_msg_translator(player)
    client.send((message+"\n").encode())

def init_client():
    """
    Initilize client side socket
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Create new player
    player = Player('Bob', 18)

    # Send the player data to server
    client_thread = threading.Thread(target=send_player_data, args=(client,player,))
    client_thread.start()

init_client()

# End of file
