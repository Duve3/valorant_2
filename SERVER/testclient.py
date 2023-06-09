import socket

HEADER = 2048
# override in case of different address or tcp tunnels
SERVER = '127.0.0.1'
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
DISCONNECT_RESPONSE = "DISCONNECTED"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response = client.recv(2048).decode(FORMAT)
    if response == message:
        print("WARNING: server echoed response sent by client!")
    if response != DISCONNECT_RESPONSE:
        return response


msg2send = input("What to send?: ")
while msg2send != ":qa":
    print(f"Result: {send(msg2send)}")
    msg2send = input("What to send?: ")

print("Exiting...")
send(DISCONNECT_MESSAGE)
