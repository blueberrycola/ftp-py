import socket
import time
import os

'''
TODO:
The client program presents a command line interface that allows a user to:
Command Line Interface Outline [X]
(C)onnect to a server [X]
(L)ist files located at the server. [X]
(G)et (retrieve) a file from the server. [X]
(S)end (put) a file from the client to the server. [X]
(T)erminate the connection to the server. [X]
REFORMAT COMMANDS TO FIT RUBRIC instead of single chars []
'''
FORMAT = 'utf-8'
HEADER = 1024   #Length of bytes
PATH = os.path.dirname(os.path.abspath(__file__))
HOST = socket.gethostbyname(socket.gethostname())
c = 'C'
l = 'L'
g = 'G'
s = 'S'
t = 'T'
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_len = str(msg_length).encode(FORMAT)
    send_len  += b' ' *(HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Variables for server addr and port
server_address = ""

#Command line interface
done = False
while(not done):
    print('Command List:')
    print('C: Connect to server,')
    print('L: List files at the server,')
    print('G: Get a file from server,')
    print('S: Send a file to server,')
    print('T: Terminate connection to the server,')
    print()
    commChar = input('Please enter a command: ')
    
    if commChar == c:
        #Connect to server
        addr = input('Please enter server ip: ')
        port = int(input('Please enter port: '))
        server_address = addr
        address = (addr, port)
        client.connect(address)

    elif commChar == l:
        #List files
        print('Listing files: ')
        #Send list command to server
        send(commChar)
        #Find the amount of strings the server will relay to client
        len = client.recv(HEADER).decode(FORMAT)
        len = int(len)
        #Loop goes for how many files are in the directory
        for i in range(0, len):
            print("FILE: ")
            print("\t" + "" + client.recv(HEADER).decode(FORMAT))
        
        
    elif commChar == g:
        #Send get command to server
        send(commChar)
        #Send req filename to server
        filename = input('Please enter filename: ')
        client.send((bytes)(filename, 'utf-8'))
        #Recieve "#" to confirm file is found
        ctrl_val = client.recv(HEADER).decode(FORMAT)

        #If server tell us we have file start loop
        if ctrl_val == '#':
            #Create data socket for retrieving file from server
            datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            datasocket.bind((addr, 47004))
            datasocket.listen()
            datasocket, address = datasocket.accept()
            print("Client server socket is listening for data")

            #Make file
            full_file = os.path.join(PATH, filename)
            print("Directory of file:" + " " + full_file)
            f = open(full_file, 'w')
            data = datasocket.recv(HEADER).decode(FORMAT)
            print("Recieved data:" + " " + data)
            f.write(data)
            print("Recieved data!" + " " + data)
            #Close file
            f.close()
            print("File recieved")
            #Close data connection
            datasocket.close()
    elif commChar == s:
        #Tell server you want to send a file and to listen for filename
        send(commChar)
        filename = input('Please enter the filename: ')
        
        #File found sending filename
        client.send((bytes)(filename, FORMAT))
        #Create data socket for sending file to server
        datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        datasocket.bind((addr, 47005))
        datasocket.listen()
        datasocket, address = datasocket.accept()
        print("Client server socket is listening for data")
        #Detect if file is found
        try:
            file = open(filename, 'rb')
            line = file.read(HEADER)
            while line:
                #Send line to client
                print(line)
                datasocket.send(line)
                line = file.read(HEADER)
            file.close()
        except IOError:
            print("File not found")
        finally:
            #Close file and connection
            datasocket.close()
        
        
        
    elif commChar == t:
        #terminate connection
        send(commChar)
        done = True
exit()
