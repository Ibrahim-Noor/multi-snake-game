import socket
import threading
from _thread import *
from player import Player
import pickle
import random
import sys

num_of_players = 2
players = []
server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
if len(players) < num_of_players:
    s.listen(num_of_players + 2)
print("waiting for connection, Server started: ")

list_of_org_of_players = []
x = 0
y = 0
foodx = 0
foody = 0
while 1:
    foodx = random.randint(10, 490)
    foody = random.randint(10, 490)
    break
for i in range(num_of_players):
    while 1:
        x = random.randint(10, 490)
        y = random.randint(10, 490)
        xy = (x, y)
        if xy not in list_of_org_of_players:
            list_of_org_of_players.append(xy)
            break
    col=(random.randint(0,32),random.randint(0,256), random.randint(0,32))
    players.append(Player(x, y, i, foodx, foody, col))

datanottosend=[]
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = []
    newcords = "0:0"
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
        #except:
        #   pass
        #try:
            players[player] = data
            if players[player].playerkilled > -1:
                killthatman = "dead"
                try:
                    all_connectiions[players[player].playerkilled].sendall(pickle.dumps(killthatman))
                except:
                    pass
                players[player].playerkilled = -1
            if players[player].eatenfood == True:
                del list_of_org_of_players[0]
                while 1:
                    foodx = random.randint(0, 490)
                    foody = random.randint(0, 490)
                    xy = (foodx, foody)
                    if xy not in list_of_org_of_players:
                        list_of_org_of_players.insert(0, xy)
                        break
                newcords = str(foodx) + ":" + str(foody)
                print("sending: ", newcords)
                for i in range(len(all_connectiions)):
                    if i not in datanottosend:
                        try:
                            all_connectiions[i].sendall(pickle.dumps(newcords))
                        except:
                            pass
            if players[player].life_status=="dead":
                datanottosend.append(player)
                break
            else:
                reply.clear()
                for i in range(len(players)):
                    if players[i].id == player or i in datanottosend:
                        pass
                    else:
                        reply.append(players[i])
                print("received: ", data)
                print("sending: ", reply)
                # for conn in all_connectiions:
                try:
                    all_connectiions[player].sendall(pickle.dumps(reply))
                except:
                    pass
        except:
            print("an error occured")
            break
            # conn.close()

    print("closing connection")
    conn.close()

current_player = 0
all_connectiions = []
thread = []
while True:
    conn, addr = s.accept()
    all_connectiions.append(conn)
    print("connected to " + str(addr))
    t = threading.Thread(target=threaded_client, args=(conn, current_player))
    thread.append(t)
    # start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
    if len(thread) == num_of_players:
        for i in range(len(thread)):
            thread[i].start()
        break