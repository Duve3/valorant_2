import socket
import pickle
import pygame

from src import constants


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.DisconnectMSG = "!!!Disconnect"
        self.DisconnectRES = "Disconnected"
        self.header = 4096
        self.encoding = "utf-8"

        self.p = self.connect()

    def getSelfPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(self.header))
        except Exception as e:
            print(f"l24 - {e = }")
            pass

    def sendPlayerData(self, data):
        try:
            freshData = (data.x, data.y)
            self.client.send(pickle.dumps(freshData))
            playerList = self.client.recv(self.header)
            selfData = self.client.recv(self.header)
            print(f"{selfData = }, {playerList = }")
            return pickle.loads(playerList), pickle.loads(selfData)
        except socket.error as e:
            print(f"l32 - {e = }")

    def disconnect(self):
        try:
            self.client.send(self.DisconnectMSG.encode(self.encoding))
            res = self.client.recv(self.header)
            if res != self.DisconnectRES.encode(self.encoding):
                print("WARNING: Server did not respond with proper response on disconnect!\nDisconnecting Anyways...")
        except socket.error as e:
            print(f"l41 - {e = }")


if __name__ == "__main__":
    screen = pygame.display.set_mode([500, 500])
    fpsClock = pygame.time.Clock()
    fps = 60
    run = True
    client = Client()
    player = client.getSelfPlayer()
    playerList = []
    while run:
        fpsClock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.disconnect()
                run = False

        # logic
        keys = pygame.key.get_pressed()

        player.handleMovement(keys)

        # rendering
        screen.fill(constants.white)

        player.draw(screen, wireframe=True)

        for plr in playerList:
            plr.draw(screen, wireframe=True)

        pygame.display.flip()

        playerList, player = client.sendPlayerData(player)
