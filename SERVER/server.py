import socket
from _thread import *
from player import Player
from player import Agents
import pickle
import pygame

encoding = "utf-8"
DisconnectMSG = "!!!Disconnect"
DisconnectRES = "Disconnected"

# antiCheat
MAX_X_MOVEMENT_PF = 10
MAX_Y_MOVEMENT_PF = 10


server = "127.0.0.1"
port = 5556
header = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started")


playerList = {}


def threaded_client(conn, pid):
    if pid in playerList:
        conn.send(pickle.dumps(playerList[pid]))
    else:
        newPlayer = Player(pid, 0, 0, ["MA", "MB", "MC"], Agents.JETT)
        conn.send(pickle.dumps(newPlayer))
        playerList[pid] = newPlayer

    # create rank based on player ip?
    ip = conn.getpeername()[0]

    nums = ip.split(".")

    total = sum([int(num) for num in nums])

    rank = total // 4  # floor divide

    print(f"{rank = }")

    while True:
        try:
            data = conn.recv(header)

            if data == DisconnectMSG.encode(encoding):
                print("Disconnected")
                del playerList[pid]
                conn.send(DisconnectRES.encode(encoding))
                break
            else:
                reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            DataPickled = pickle.loads(data)

            print("Received: ", data)
            print("Sending : ", reply)
            try:
                print(f"{(reply[0].x, reply[0].y) = }")
            except IndexError as ee:
                print(f"l69 - {ee = }")
            # data checks
            ACR = ""
            if abs(playerList[pid].x - DataPickled[0]) > MAX_X_MOVEMENT_PF:  # moved more than ~ units in 1 frame
                playerList[pid].x = playerList[pid].x
                ACR = "MAX_X_MOVEMENT_PF EXCEEDED"
            else:
                playerList[pid].x = DataPickled[0]  # x

            if abs(playerList[pid].y - DataPickled[1]) > MAX_Y_MOVEMENT_PF:
                playerList[pid].y = playerList[pid].y
                ACR = "MAX_Y_MOVEMENT_PF EXCEEDED"
            else:
                playerList[pid].y = DataPickled[1]  # y
            playerList[pid].update()  # update rect

            if ACR != "":
                print("ANTICHEAT: Triggered on player id:", pid, "with reason:\"", ACR, "\"")

            # game logic
            collisionList = [pygame.Rect(plr.rect) for plr in reply]
            collision = pygame.Rect.collidelist(pygame.Rect(playerList[pid].rect), collisionList)
            if collision != -1:
                print(f"{collision = }")
                print(f"{collisionList = }")
                print(f"{[playerList.keys()] = }")
                collideID = [key for key in playerList.keys()].index(reply[collision].id)  # we are doing key for key ... because we are trying to avoid getting a dict_keys object from the playerList.keys()
                print(f"{collideID = }")
                playerList[collideID].health -= 0.1

            for plr in playerList.values():
                plr.width = abs(plr.health // 2)
                plr.height = abs(plr.health // 2)



            # refresh reply
            reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            print(f"{playerList[pid].__vars__() = }")

            conn.sendall(pickle.dumps(reply))
            conn.sendall(pickle.dumps(playerList[pid]))

        except Exception as err:
            print(f"{err = }")
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
