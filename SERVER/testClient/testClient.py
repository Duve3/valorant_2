"""
Test client, it is essentially the game but just stripped down to the client level. The player object must be duplicated on both the server and player side.
"""

import socket
import pygame
from player import Player, JSONToPlayer, playerToJSON
from constants import setupLogger, DisconnectMSG, DisconnectRES, encoding
import logging

logger = logging.getLogger("testclient-0")
logger = setupLogger(logger)


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 108
        self.addr = (self.server, self.port)
        self.header = 1024
        self.client.settimeout(10)

        self.p = self.connect()

    def getSelfPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.recv()
            logger.debug(f"data: {data}")  # data will purposely not go into file because it will crash pycharm
            return JSONToPlayer(data)
        except Exception as e:
            logger.error(e)
            raise e

    def sendPlayerData(self, plr):
        try:
            self.send(playerToJSON(plr))

            Nplayer = JSONToPlayer(self.recv())
            NplayerList = []
            msg = self.recv()
            logger.debug(f"msg: {msg}")
            if msg != "[]":
                for lp in msg.splitlines():
                    logger.debug(f"LP: {lp}")
                    NplayerList.append(JSONToPlayer(lp))

            return Nplayer, NplayerList

        except Exception as e:
            logger.error(e)
            raise e

    def disconnect(self):
        try:
            self.send(DisconnectMSG)
            res = self.recv()
            if res != DisconnectRES:
                logger.warning("WARNING: Server did not respond with proper response on disconnect!\nDisconnecting Anyways...")
        except Exception as e:
            logger.error(e)
            raise e

    def send(self, msg):
        message = msg.encode(encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(encoding)
        send_length += b' ' * (self.header - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def recv(self) -> str:
        length = int(self.client.recv(self.header).decode(encoding))  # if it doesn't int that means something went really wrong so its ok to crash
        logger.debug(f"received byte length of {length}")
        return self.client.recv(length).decode(encoding)


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
        screen.fill("white")

        player.draw(screen, wireframe=True)

        for plr in playerList:
            logger.debug(f"PID: {plr.id}, pos: ({plr.x}, {plr.y})")
            plr.draw(screen, wireframe=True)

        pygame.display.flip()

        player, playerList = client.sendPlayerData(player)
