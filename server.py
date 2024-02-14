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

players = [Player(0,0,50,50, (255,0,0)), Player(100,100,50,50, (0,0,255)),
           Player(200,200,50,50, (0,255,0))]

def threaded_client(conn, client_id):
    global players
    conn.send(pickle.dumps(players[client_id]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[client_id] = data

            if not data:
                print("Disconnected")
                break
            else:

                # for i in players:
                #     if client_id == i:
                #         reply = players
                #         if players[i] in reply:
                #             reply.remove(players[i])
                if client_id == 0:
                    reply = [players[1], players[2]]
                elif client_id == 1:
                    reply = [players[0], players[2]]
                elif client_id == 2:
                    reply = [players[0], players[1]]


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

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
