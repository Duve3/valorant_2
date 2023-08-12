import socket
import threading
count = 0 
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode
    send_length += b' ' * (HEADER - len(msg_length))
    server.send(send_length)
    server.send(message)
HEADER = 64
PORT = 5050
SERVER = "192.168.1.27"
FORMAT = "utf-8"
ADDR = (SERVER,PORT)
dcmsg = "DIS"
players = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(SERVER)
server.bind(ADDR)
def sendclient():
    pass
class PLAYER():
    def __init__(self, addr) -> None:
        self.id = count
        count += 1
        self.addr = addr
        self.x = None
        self.y = None
        players.append(self)
        
def handle_client(conn,addr): #THIS RUNS ONCE PER CLIENT
    Client = PLAYER(addr)
    conn.send()
    connected = True
    while connected:
        
        LONGNESS = conn.recv(HEADER).decode(FORMAT)#must be less then 64 thingy
        try:
            LONGNESS = int(LONGNESS)
        except:
            print("bruh")
        if not LONGNESS == "":
            
            msg = conn.recv(LONGNESS).decode(FORMAT)
            msgaf
            if msg.startswith("P"):
                x,y = msg.split(";")
                Client.x = x
                Client.y = y
                
                
            if msg.startswith("P"):
                msgaf = msgaf.split(",")
                for i in range(len(msgaf)):
                    one,two = msgaf[i].split(';')
                    msgaf[i] = (one,two)
                
            if msg == dcmsg:
                connected = False
        
    conn.close()
def start():
    server.listen()
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
thread = threading.Thread(target=sendclient)
print("STARTING NERDS")
start()