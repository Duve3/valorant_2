import socket
import threading
import sys

server = ""
port = 5000
header = 2048  # bytes or bits idk
encoding = "utf-8"
disconnect_msg = "!DISCONNECT"
disconnect_res = "DISCONNECTED"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    print(f"FATAL ERROR:\n\t{str(err)}")

idCounter = 0


def handle(conn, addr):
    global idCounter

    while True:
        try:
            data = conn.recv(header)
            msg = data.decode(encoding)
            print(f"[{addr}] - {msg}")

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
        thread.join(10)
