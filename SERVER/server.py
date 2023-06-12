import socket
import threading
import json

server = ""
port = 5000
header = 2048  # bytes or bits idk
encoding = "utf-8"
disconnect_msg = "!DISCONNECT"
disconnect_res = "DISCONNECTED"
PlayerData_MSG = "PLAYERDATA:"
PlayerData_RES = "RECEIVED"
ReqData_MSG = "REQDATA"
NewID_MSG = "GIVEID"
NewID_RES = "ID:"
SelfData_MSG = "SELFDATA:"
SelfData_RES = "DATA:"
Joining_MSG = "JOINING:"
Joining_RES = "JOINING"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    print(f"FATAL ERROR:\n\t{str(err)}")

idCounter = 0

playerData = {}


def playerDataHandler(givenData: str):
    global playerData

    givenData = givenData.replace(PlayerData_MSG, "")
    givenData = givenData.replace("'", '"')  # replace '' to "" since ' isn't allowed in json

    print(f"On FINAL for loads, data:\n\t{givenData}")
    Dictionary = json.loads(givenData)  # load the playerData into json format (dictionary)
    playerData = Dictionary
    return playerData


def returnSelfData(pid: int):
    global playerData

    return playerData[pid]


def idHandler():
    global idCounter
    idCounter += 1
    return idCounter - 1


def handle(conn: socket.socket, addr):
    plrData = {}

    while True:
        msg_length = conn.recv(header).decode(encoding)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encoding)
            print(f"[{addr}] - {msg} with length: {msg_length}")
            if msg == disconnect_msg:
                conn.send(disconnect_res.encode(encoding))

            elif msg.startswith(PlayerData_MSG):
                plrData = playerDataHandler(msg)
                conn.send(PlayerData_RES.encode(encoding))

            elif msg == ReqData_MSG:
                conn.send(str(plrData).encode(encoding))

            elif msg == NewID_MSG:
                newID = idHandler()
                conn.send(str(newID).encode(encoding))

            elif msg.startswith(SelfData_MSG):
                selfData = returnSelfData(int(msg.replace(SelfData_MSG, "")))
                conn.send(str(selfData).encode(encoding))

            else:
                conn.send(msg.encode(encoding))


def listen():
    s.listen()
    print("Waiting...")
    while True:
        conn, addr = s.accept()
        print(f"New connection: {conn}, {addr}")

        thread = threading.Thread(target=handle, args=(conn, addr), daemon=True)
        thread.start()
        print(f"There is currently: {threading.activeCount() - 1} clients!")
        thread.join()  # removed timeout for testing purposes


if __name__ == "__main__":
    listen()
