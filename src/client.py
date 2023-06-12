import socket
import json
from player import Player

HEADER = 2048
# override in case of different address or tcp tunnels
SERVER = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
DISCONNECT_RESPONSE = "DISCONNECTED"
PlayerData_MSG = "PLAYERDATA:"
PlayerData_RES = "RECEIVED"
ReqData_MSG = "REQDATA"
NewID_MSG = "GIVEID"
NewID_RES = "ID:"
SelfData_MSG = "SELFDATA:"
SelfData_RES = "DATA:"
Joining_MSG = "JOINING:"
Joining_RES = "JOINING"

ADDR = (SERVER, PORT)  # NOQA:DUPCODEFRAG
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def __send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)
    if response.encode(FORMAT) == message:
        print("WARNING: server echoed response sent by client!")
    if response != DISCONNECT_RESPONSE:
        return response


def plrDataSend(plr: Player, pid: int):
    # ex: {"health": 12, "dps": 10682, "targetID": 27}
    data = {
        "id": pid,
        "x": plr.x,
        "y": plr.y,
        "model": plr.currentModel,
        "agent": plr.agent
    }

    res = __send(f"{PlayerData_MSG}{data}")

    if res != PlayerData_RES:
        print("WARNING: FAILED TO RECEIVE PROPER RESPONSE FOR PLAYER DATA SEND")


def plrDataGet():
    plrData = __send(ReqData_MSG)

    return json.loads(plrData)


def getSelfData(pid: int):
    selfData = __send(f"{SelfData_MSG}{pid}")

    return json.loads(selfData.replace(f"{SelfData_RES}", ""))


def getID():
    pid = __send(NewID_MSG)

    return pid.replace(f"{NewID_RES}", "")

