import socket
from _thread import *
import pickle

# set up address
server = "localhost"
port = 20

# make socket
s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)

# bind socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# listen for some connections
MAX_PLAYERS = 5
s.listen(MAX_PLAYERS)
data_size = 2048
print("Waiting for a connection, Server Started")

# list of all available players
start_player_data = {0:{"ID":0, "x":50, "y":0, "active":False},
                     1:{"ID":1, "x":100, "y":0, "active":False},
                     2:{"ID":2, "x":150, "y":0, "active":False},
                     3:{"ID":3, "x":200, "y":0, "active":False},
                     4:{"ID":4, "x":250, "y":0, "active":False}}
all_player_data = {}
closed_player_list = []
closed_player_id = None

# our connection to the clients
def threaded_client(conn, client_id):
    global start_player_data, closed_player_id, all_player_data

    # Send initial player data to the client
    conn.send(pickle.dumps(start_player_data[client_id]))

    while True:
        try:
            # receive data from client
            data = pickle.loads(conn.recv(data_size))

            # interpret data
            if type(data) == dict:
                all_player_data[client_id] = data
            else:
                closed_player_id = data
                closed_player_list.append(closed_player_id)
                closed_player_list.sort()
                print(f"Closed:{closed_player_id}")

            # if no data to receive
            if not data:
                print("Disconnected")
                # Send the reply to the client
                conn.sendall(pickle.dumps(reply))
                break
            else:
                if all_player_data[client_id]["active"] == False:
                    all_player_data.pop(client_id)

                # Create a reply containing other players' data
                reply = {}
                for key, value in all_player_data.items():
                    if key != client_id and value["active"] == True:
                        reply[key] = value

                # Send the reply to the client
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

    # so we don't get over MAX_PLAYER limit
    if currentPlayer >= MAX_PLAYERS:
        currentPlayer = MAX_PLAYERS

    # figure out what player to use next
    if len(closed_player_list) == 0:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
    else:
        start_new_thread(threaded_client, (conn, closed_player_list[0]))
        closed_player_list.pop(0)

    # so we don't get over MAX_PLAYER limit
    if currentPlayer >= MAX_PLAYERS:
        currentPlayer = 0

    # print out which player
    print("Current one:" + str(currentPlayer))
