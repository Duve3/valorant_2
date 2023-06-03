import socket
import threading
import sys

server = ""
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(f"FATAL ERROR:\n\t{str(e)}")

s.listen()

def handle(conn):
    pass
