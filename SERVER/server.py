import socket
from _thread import start_new_thread
from player import Player
from player import Agents
from antiCheat import checkValues
import pickle
import pygame

encoding = "utf-8"
DisconnectMSG = "!!!Disconnect"
DisconnectRES = "Disconnected"


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

            # print("Received: ", data)
            # print("Sending : ", reply)
            # try:
            #     print(f"{(reply[0].x, reply[0].y) = }")
            # except IndexError as ee:
            #     print(f"l69 - {ee = }")

            # antiCheat
            checkValues(DataPickled, playerList, pid)
            playerList[pid].update()  # update rect

            # game logic
            """
            collisionList = [pygame.Rect(plr.rect) for plr in reply]
            collision = pygame.Rect.collidelist(pygame.Rect(playerList[pid].rect), collisionList)
            if collision != -1:
                collideID = [key for key in playerList.keys()].index(reply[collision].id)  # we are doing key for key ... because we are trying to avoid getting a dict_keys object from the playerList.keys()
                if playerList[collideID].iframes <= 0:
                    playerList[collideID].health -= 1
                    playerList[collideID].iframes = 5
            """

            # refresh reply
            reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            # print(f"{playerList[pid].__vars__() = }")
            playerList[pid].iframes = playerList[pid].iframes - 1 if playerList[pid].iframes > 0 else 0

            conn.sendall(pickle.dumps(reply))
            conn.sendall(pickle.dumps(playerList[pid]))

        except Exception as err:
            raise err

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    connection, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (connection, currentPlayer))
    currentPlayer += 1
