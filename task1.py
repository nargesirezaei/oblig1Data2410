from socket import *
import sys

# since server running on our local pc, we will use localhost and a spesific 
#port number for server running on 
HOST = '127.0.0.1'
PORT = 8001


 
#preparing a server socket and binding it to host and port
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))

#a web server that handles one HTTP request at a time
server_socket.listen(1)
print(f'Server is listening on {HOST}:{PORT}')

while True:
    #accepting the request from client and we will have thems ip too
    connectionSocket, addr = server_socket.accept()
    print(f'Accepted connection from {addr}')

    try:
        #recieving the http request from client. and giving 1024 bit for msg
        message = connectionSocket.recv(1024)
        request_text = message.decode('utf-8')

        #This code is used to read the file requested in an HTTP request message.
        #this extranct the file name from the http request
        filename = message.split()[1] 
        #opens the file in read mode.
        # is used to remove the initial forward slash (/) from the filename.
        f = open(filename[1:])
        #reads the contents of the file and stores it in the outputdata variable.
        outputdata = f.read()


        #This is an HTTP response message that indicates a successful request.
        message = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(message.encode())

        

        #Send the content of the requested file to the client
        #Once all the characters have been sent, a final "\r\n".encode()
        #is sent to indicate the end of the response message. 
        #Finally, the connection socket is closed to free up system resources.
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        #when the requested file does not exist on the server,send a 404 Not Found response
        #The server then sends the message back to the client by encoding it
        #into bytes, sending it over the connection socket, and then closing 
        #the connection socket.
        message = "HTTP/1.1 404 Not Found\r\n"
        message += "Content-Type: text/html\r\n\r\n"
        message += "<h1>404 Not Found</h1>"
        connectionSocket.send(message.encode())
        connectionSocket.close()

    server_socket.close() 
    sys.exit()  
    #terminate the program