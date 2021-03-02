import socket
import threading
import ftplib
import os


HEADER = 1024   #Length of bytes 
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
PATH = os.path.dirname(os.path.abspath(__file__))
print("Path:" + " " + PATH)
FTP_PATH = ""
FTP_PATH = FTP_PATH + PATH + "\\ftpdir"
print("Path:" + " " + FTP_PATH)
C_MESSAGE = "C"
DC_MESSAGE = "T" #Disconnect client to server
LIST_MESSAGE = "L" #List files available for download to client
GET_MESSAGE = "G" #Prompt user for filename and get file if in server
SEND_MESSAGE = "S" #Send a file to the server that it can host
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print(ADDR)

def handle_client(connection, addr):
    print(f"\t[NEW CONNECTION]: {addr}")
    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == C_MESSAGE:
                start()
            if msg == LIST_MESSAGE:
                print(f"Sending File Info to {addr}")
                #Use os to list files found in FTP_DIRECTORY, send to client
                files = os.listdir(FTP_PATH)
                file_len = str(len(files))
                #Send the file length to client so it knows how many messages it will recv
                file_len = (bytes)(file_len, 'utf-8')
                connection.send(file_len)

                print(files)
                for f in files:
                    str_byte = (bytes)(f, 'utf-8')
                    connection.send(str_byte)
                    print(f)
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

