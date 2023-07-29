"""
Test client, it is essentially the game but just stripped down to the client level. The player object must be duplicated on both the server and player side.
"""

import socket
import pickle
import pygame
from src import constants
from SERVER.constants import PlayerListSTART, PlayerListEND, PlayerEND, PlayerSTART, DisconnectMSG, DisconnectRES, encoding
from player import Player

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.header = 4096
        self.client.settimeout(10)

        self.p = self.connect()

    def getSelfPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = b""
            if self.client.recv(self.header) == PlayerSTART.encode(encoding):
                while True:
                    packet = self.client.recv(self.header)
                    if packet == PlayerEND.encode(encoding):
                        break
                    data += packet
                    print("packet", packet)
            print("data:", data)
            return pickle.loads(data)
        except Exception as e:
            print(f"l24 - {e = }")
            raise e

    def sendPlayerData(self, data):
        try:
            freshData = (data.x, data.y)
            self.client.send(pickle.dumps(freshData))
            plrList = b""
            if self.client.recv(self.header) == PlayerListSTART.encode(encoding):
                while True:
                    packet = self.client.recv(self.header)
                    if packet == PlayerListEND.encode(encoding):
                        break
                    plrList += packet

            rplr = b""
            if self.client.recv(self.header) == PlayerSTART.encode(encoding):
                while True:
                    packet = self.client.recv(self.header)
                    if packet == PlayerEND.encode(encoding):
                        break
                    rplr += packet

            print(f"{rplr = }, {plrList = }")
            return pickle.loads(plrList), pickle.loads(rplr)
        except socket.error as e:
            print(f"l32 - {e = }")
            raise e

    def disconnect(self):
        try:
            self.client.send(DisconnectMSG.encode(encoding))
            res = self.client.recv(self.header)
            if res != DisconnectRES.encode(encoding):
                print("WARNING: Server did not respond with proper response on disconnect!\nDisconnecting Anyways...")
        except socket.error as e:
            print(f"l41 - {e = }")


if __name__ == "__main__":
    screen = pygame.display.set_mode([500, 500])
    fpsClock = pygame.time.Clock()
    fps = 60
    run = True
    client = Client()
    player: Player = client.getSelfPlayer()
    playerList = []
    while run:
        fpsClock.tick(fps)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                client.disconnect()
                run = False

        if not run:  # auto break on run false
            break

        # logic
        # auto hook events
        player.hookEvents(events)

        # rendering
        screen.fill(constants.white)

        player.draw(screen, wireframe=True)

        for plr in playerList:
            plr.draw(screen, wireframe=True)

        pygame.display.flip()

        playerList, player = client.sendPlayerData(player)
