import socket
from _thread import *
from player import Player
import pickle

# set up address
server = "127.0.0.1"
port = 20

# make socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listen for some connections
MAX_PLAYERS = 4
s.listen(MAX_PLAYERS)
print("Waiting for a connection, Server Started")

# list of all available players
players = [Player(0,0,50,50, (255,0,0), 1), Player(100,100,50,50, (0,0,255), 2),
           Player(200,200,50,50, (0,255,0), 3), Player(300,100,50,50, (255,255,0), 4)]
closed_player_id = None

# our connection to the clients
def threaded_client(conn, client_id):
    global players, closed_player_id, currentPlayer

    # send initial player to client
    conn.send(pickle.dumps(players[client_id]))
    reply = ""

    while True:
        try:
            # receive data from client
            data = pickle.loads(conn.recv(2048))

            # interpret data
            if type(data) == Player:
                players[client_id] = data
            else:
                closed_player_id = data - 1
                print(closed_player_id)

            if not data:
                print("Disconnected")
                break
            else:
                # make a reply for the client
                if client_id == 0:
                    reply = [players[1], players[2], players[3]]
                elif client_id == 1:
                    reply = [players[0], players[2], players[3]]
                elif client_id == 2:
                    reply = [players[0], players[1], players[3]]
                elif client_id == 3:
                    reply = [players[0], players[1], players[2]]

            # send reply to client
            conn.sendall(pickle.dumps(reply))

        except:
            break

    # if client leaves
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    # connect to client
    conn, addr = s.accept()
    print("Connected to:", addr)

    # figure out what player to use next
    if closed_player_id == None:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
    else:
        start_new_thread(threaded_client, (conn, closed_player_id))
        closed_player_id = None

    # so we don't get over MAX_PLAYER limit
    if currentPlayer >= MAX_PLAYERS:
        currentPlayer = MAX_PLAYERS

    # print out which player
    print("Current one:" + str(currentPlayer))

