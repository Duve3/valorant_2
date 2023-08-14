import socket
import time
from _thread import start_new_thread
from player import Player, Agents, Models, Rifle
import antiCheat as ac
import pickle
import pygame
from constants import PlayerListSTART, PlayerListEND, PlayerEND, PlayerSTART, DisconnectMSG, DisconnectRES, encoding, setupLogger
import logging

server = "127.0.0.1"
port = 5556
header = 2048 * 120  # 240 kb of data read
playerList: dict[Player] = {}
playerDefaults = [0, 0, Agents.JETT]


def copyGameStatus():
    pygame.init()
    screen = pygame.display.set_mode([500, 500], pygame.HIDDEN)


def threaded_client(conn, pid, logger):
    newPlayer = Player(pid, 0, 0, Agents.JETT)
    playerList[pid] = newPlayer
    conn.sendall(pickle.dumps(newPlayer))

    rank = sum([int(num) for num in conn.getpeername()[0].split('.')]) // 4
    logger.info(f"{rank = }")
    # rank system ^ not actually working currently

    while True:
        try:
            data = conn.recv(header)

            if data == DisconnectMSG.encode(encoding):
                logger.info("Disconnected")
                del playerList[pid]
                conn.send(DisconnectRES.encode(encoding))
                break

            DataPickled = pickle.loads(data)
            logger.debug("received:", DataPickled)
            logger.debug("playerList:", playerList)

            # ac
            ac.checkValues(DataPickled, playerList, pid)
            playerList[pid].update()

            # game logic
            logger.debug(playerList[pid].__dict__)
            for gun in playerList[pid].weapons:
                gun.tick()

            reply = [x for i, x in enumerate(playerList.values()) if i != pid and x is not None]

            playerList[pid].iframes = playerList[pid].iframes - 1 if playerList[pid].iframes > 0 else 0

            conn.sendall(pickle.dumps((reply, playerList[pid])))

        except Exception as err:
            raise err

    logger.info("Connection Closed")
    conn.close()


def main():
    logger = logging.getLogger("server-0")
    logger = setupLogger(logger)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((server, port))

    s.listen()
    logger.info("Waiting for connection")

    currentPlayer = 0
    while True:
        connection, addr = s.accept()
        logger.info("Connected to:", addr)

        CL = logging.getLogger(f"server-{currentPlayer + 1}")
        CL = setupLogger(CL)
        start_new_thread(threaded_client, (connection, currentPlayer, CL))
        currentPlayer += 1


if __name__ == '__main__':
    copyGameStatus()
    main()


