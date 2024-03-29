import socket
import ipaddress
from _thread import start_new_thread
from player import Player, Agents, JSONToPlayer, playerToJSON, Ranks
import antiCheat
import pygame
from constants import DisconnectMSG, DisconnectRES, encoding, setupLogger
import logging

server = "127.0.0.1"
port = 5555
header = 1024
playerList: dict[Player] = {}


def copyGameStatus():
    pygame.init()
    pygame.display.set_mode([500, 500], pygame.HIDDEN)


def send(msg: str, conn: socket.socket):
    message = msg.encode(encoding)
    msg_length = len(message)
    send_length = str(msg_length).encode(encoding)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(message)


def recv(conn) -> str:
    length = int(conn.recv(header).decode(encoding).replace(" ", ''))  # if it doesn't int that means something went really wrong, so it's ok to crash

    return conn.recv(length).decode(encoding)


def calculate_rank(avg: int) -> str:
    avg *= 10
    avg //= 100

    return Ranks.fromValue(avg)


def threaded_client(conn, pid, logger):
    newPlayer = Player(pid, 0, 0, Agents.JETT)
    playerList[pid] = newPlayer
    send(playerToJSON(newPlayer), conn)

    if type(ipaddress.ip_address(conn.getpeername()[0])) == ipaddress.IPv4Address:
        RawRank = sum([int(num) for num in conn.getpeername()[0].split('.')]) // 4
    else:
        RawRank = 0  # ranks are just skipped for ipv6 ips due to the weird alphanumeric chars.

    rank = calculate_rank(RawRank)
    logger.info(f"{rank = }, {RawRank = }")
    # rank system ^ not actually working currently

    while True:
        try:
            data = recv(conn)

            if data == DisconnectMSG:
                logger.info("Disconnected")
                del playerList[pid]
                send(DisconnectRES, conn)
                break

            plrData = JSONToPlayer(data)
            logger.debug(f"received: {data}")
            logger.debug(f"playerList: {playerList}")

            # ac
            antiCheat.checkValues(plrData, playerList, pid)

            # game logic
            logger.debug(playerList[pid].__dict__)
            for gun in playerList[pid].weapons:
                gun.tick()

            reply = ""
            for i, x in enumerate(playerList.values()):
                if i != pid and x is not None:
                    reply += f"{playerToJSON(x)}\n"

            playerList[pid].iframes = playerList[pid].iframes - 1 if playerList[pid].iframes > 0 else 0

            send(playerToJSON(playerList[pid]), conn)
            send(str(reply), conn)

        except Exception as err:
            raise err

    logger.info("Connection Closed")
    conn.close()


def main():
    OverAllListeningLevel = logging.DEBUG
    logger = logging.getLogger("server-0")
    logger = setupLogger(logger, level=OverAllListeningLevel)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.bind((server, port))
    except OSError:
        logger.error(f"Failed binding to {server}:{port}.")
        logger.info("Reattempting binding to a port 1 higher!")
        s.bind((server, port + 1))

    s.listen()
    logger.info("Waiting for connection")

    currentPlayer = 0
    while True:
        connection, addr = s.accept()
        logger.info(f"Connected to: {addr}")

        CL = logging.getLogger(f"server-{currentPlayer + 1}")
        CL = setupLogger(CL, level=OverAllListeningLevel)
        start_new_thread(threaded_client, (connection, currentPlayer, CL))
        currentPlayer += 1


if __name__ == '__main__':
    copyGameStatus()
    main()
