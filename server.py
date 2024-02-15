import socket
from _thread import *
from player import Player
import pickle

server = "127.0.0.1"
port = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")

MAX_PLAYERS = 4
players = [Player(0,0,50,50, (255,0,0), 1), Player(100,100,50,50, (0,0,255), 2),
           Player(200,200,50,50, (0,255,0), 3), Player(300,100,50,50, (255,255,0), 4)]

closed_player_id = 0

def threaded_client(conn, client_id):
    global players, closed_player_id
    conn.send(pickle.dumps(players[client_id]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if type(data) == Player:
                players[client_id] = data
            else:
                closed_player_id = data-1
                print(closed_player_id)

            if not data:
                print("Disconnected")
                break
            else:

                if client_id == 0:
                    reply = [players[1], players[2], players[3]]
                elif client_id == 1:
                    reply = [players[0], players[2], players[3]]
                elif client_id == 2:
                    reply = [players[0], players[1], players[3]]
                elif client_id == 3:
                    reply = [players[0], players[1], players[2]]


                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if closed_player_id == 0:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
    else:
        start_new_thread(threaded_client, (conn, closed_player_id))
        closed_player_id = 0

    if currentPlayer > MAX_PLAYERS:
        currentPlayer = MAX_PLAYERS


    print("Current one:" + str(currentPlayer))

