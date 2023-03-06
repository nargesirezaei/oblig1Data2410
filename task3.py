import socket
 #to be able to have multiple-client server
import threading



#accepting the request from client and we will have thems ip too
def handle_client(client_socket, client_address):#
    #client-request
    request = client_socket.recv(1024)

    #This is an HTTP response message that indicates a successful request.
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!\r\n"
    client_socket.sendall(response)
    

    #Closing client socket
    client_socket.close()

#infinite loop where it waits for incoming client connections. 
def serve_forever(server_host, server_port):
    # Create a TCP socket and bind it to the server address and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen()

    print("Server listening on {}:{}".format(server_host, server_port))

    while True:
      
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    serve_forever("127.0.0.1", 8080)