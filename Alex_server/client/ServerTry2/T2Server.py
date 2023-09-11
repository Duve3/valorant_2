import socket
import threading
import json
import pygame
pygame.init()
clock = pygame.time.Clock()
def sendasjson(msg,conn):
    msg = str(msg)
    msgjson = json.dumps(msg)
    message = msgjson.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)  
def sendall(msg):
    msg = str(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - msg_length)
    server.sendall(send_length)
    server.sendall(message)
def send(msg, conn):
    msg = str(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - msg_length)
    conn.send(send_length)
    conn.send(message)
HEADER = 64
PORT = 5050
SERVER = "192.168.50.145"#192.168.1.25 ,  192.168.50.145
FORMAT = "utf-8"
ADDR = (SERVER,PORT)
dcmsg = "DIS"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(SERVER)
server.bind(ADDR)
idaddr = []
players = []
def idtoaddr(id):
     return next(d["addr"] for d in idaddr if d['id'] == id)



class player:
     def __init__(self,id,addr) -> None:
        self.x = None
        self.y = None
        self.isalive = True
        self.id = id
        self.bullets = []
        idaddr.append({"id":id,"addr":addr})

        players.append(self)



def handle_client(conn,addr): #THIS RUNS ONCE PER CLIENT
    print(f"ID:{threading.active_count()} Sent to:{conn}")
    id = threading.active_count()
    send(id, conn)
    connect = player(id, conn)
    LONGNESS = conn.recv(HEADER).decode(FORMAT)#must be less then 64 thingy


    try:
        LONGNESS = int(LONGNESS)


    except:
            print("length was not a int")


    if not LONGNESS == "":
            idsent = conn.recv(LONGNESS).decode(FORMAT)



    if not str(idsent) == str(id):
         
         print(f"id:{id} sentid:{idsent}")

         conn.close()


    print(f"Connected {addr},{conn}")

    connected = True



    while connected:
        
        LONGNESS = conn.recv(HEADER).decode(FORMAT)#must be less then 64 thingy
        try:
            LONGNESS = int(LONGNESS)
        except:
            print("bruh")
        if not LONGNESS == "":
            msg = conn.recv(LONGNESS).decode(FORMAT)  # Receiving as a JSON string
            connect.bullets = []
            # ...
            data = json.loads(msg)  # Decoding as JSON
            try:
                connect.x = data[0]
                connect.y = data[1]

            except:
                 print("NOT A UPDATE TICK")

    conn.close()
        
            
def start():
    server.listen()
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
def update():
     while True:
          epic = []
          for thing in players:
               epic.append(thing.__dict__)
          for verycool in idaddr:
            sendasjson(epic, verycool["addr"])
          clock.tick(60)
thread = threading.Thread(target=update)
thread.start()
print("STARTING NERDS")
start()
