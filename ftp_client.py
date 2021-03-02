import socket

'''
TODO:
The client program presents a command line interface that allows a user to:
Command Line Interface Outline [X]
(C)onnect to a server [X]
(L)ist files located at the server. [X]
(G)et (retrieve) a file from the server. []
(S)end (put) a file from the client to the server. []
(T)erminate the connection to the server. [X]
'''
FORMAT = 'utf-8'
HEADER = 1024   #Length of bytes 
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
        #Get file
        filename = input('Please enter filename: ')
        filename = (bytes)(filename, FORMAT)
        client.send(filename)
        #Check if file present
        #If file present then recv from server and put into clientdir
        #Else throw error and return to loop
    elif commChar == s:
        #Send a file
        filename = input('Please enter the filename and extension in this directory')
        #Check if file present in client
        #If file present then send to server
        #Else throw error and return to loop
    elif commChar == t:
        #terminate connection
        send(commChar)
        done = True
exit()
