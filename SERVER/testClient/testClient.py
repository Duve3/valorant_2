"""
Test client, it is essentially the game but just stripped down to the client level. The player object must be duplicated on both the server and player side.
"""

import socket
import pickle
import pygame
from src import constants
from SERVER.constants import PlayerListSTART, PlayerListEND, PlayerEND, PlayerSTART, DisconnectMSG, DisconnectRES, encoding, setupLogger
from player import Player
import logging

logger = logging.getLogger("testclient-0")
logger = setupLogger(logger)


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.header = 2048 * 120  # 240 kb of data read.
        self.client.settimeout(10)

        self.p = self.connect()

    def getSelfPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(self.header)
            logger.debug("data:", data)  # data will purposely not go into file because it will crash pycharm
            return pickle.loads(data)
        except Exception as e:
            logger.error(e)
            raise e

    def sendPlayerData(self, data):
        try:
            freshData = (data.x, data.y)
            self.client.send(pickle.dumps(freshData))

            dataTuple: tuple = pickle.loads(self.client.recv(self.header))

            return dataTuple[0], dataTuple[1]

        except Exception as e:
            logger.error(e)
            raise e

    def disconnect(self):
        try:
            self.client.send(DisconnectMSG.encode(encoding))
            res = self.client.recv(self.header)
            if res != DisconnectRES.encode(encoding):
                logger.warning("WARNING: Server did not respond with proper response on disconnect!\nDisconnecting Anyways...")
        except Exception as e:
            logger.error(e)
            raise e


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
