import socket
import threading
import sys
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    print(f"FATAL ERROR:\n\t{str(err)}")

idCounter = 0

playerData = {}


def playerDataHandler(givenData: str):
    global playerData
    assert(isinstance(givenData, str), "Not given string data!")

    givenData.replace(PlayerData_MSG, "")
    givenData.replace("'", '"')  # replace '' to "" since ' isn't allowed in json

    Dictionary = json.loads(givenData)  # load the playerData into json format (dictionary)
    playerData = Dictionary
    return playerData


def handle(conn: socket.socket, addr):
    global idCounter
    plrData = {}

    while True:
        try:

            msg_length = conn.recv(header).decode(encoding)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(encoding)
                print(f"[{addr}] - {msg} with length: {msg_length}")
                if msg == disconnect_msg:
                    conn.send(disconnect_res.encode(encoding))

                elif msg == PlayerData_MSG:
                    plrData = playerDataHandler(msg)
                    conn.send(PlayerData_RES.encode(encoding))

                elif msg == ReqData_MSG:
                    conn.send(str(plrData).encode(encoding))



                conn.send(msg.encode(encoding))


        except Exception as e:
            print(f"FATAL ERROR:\n\t{str(e)}")


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
