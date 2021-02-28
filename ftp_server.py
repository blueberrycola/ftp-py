import socket
import threading

HEADER = 1024   #Length of bytes 
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MESSAGE = "T" #Disconnect client to server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(connection, addr):
    print(f"\t[NEW CONNECTION]: {addr}")
    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DC_MESSAGE:
                 
                 connected = False
    print(f"CONNECTION TERMINATED {addr}")
    connection.close()
    
    
        
        
        
def start():
    server.listen()
    print(f"Listening on {SERVER}")
    while True:
        connection, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, addr))
        thread.start()
        print(f"\t[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("Server is STARTING!")
start()
