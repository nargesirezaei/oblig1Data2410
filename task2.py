#i do not write same comment as task1 again.
from socket import *
import sys  
import threading



server_socket = socket(AF_INET, SOCK_STREAM)


HOST = "127.0.0.1"
PORT =6789

try:
    server_socket.bind((HOST,PORT))
except Exception as e:
    print(f"Exception: {e}")
    sys.exit()

server_socket.listen(10)
print('ready to serve')


def handle_request(connection_socket):
    while True:
        try:
            message = connection_socket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            
            message = "HTTP/1.1 404 Not Found\r\n".encode()
            message += "Content-Type: text/html\r\n\r\n".encode()
            message += "<h1>404 Not Found</h1>".encode()
            connection_socket.send(message)
            for i in range(0, len(outputdata)):
                connection_socket.send(outputdata[i].encode())
            connection_socket.send("\r\n".encode())
            connection_socket.close()
            break
        except IOError:
            
            message = "HTTP/1.1 404 Not Found\r\n"
            message += "Content-Type: text/html\r\n\r\n"
            message += "<h1>404 Not Found</h1>"
            connection_socket.send(message)
            connection_socket.close()
            break
        except ConnectionError:
            print('what ever')
            connection_socket.close()
            break
def receive():
    while True:
        try:
            
            connection_socket, addr = server_socket.accept()
            print(f'Ready to serve...')

            # Start handling thread for client to handle them at the same time
            thread = threading.Thread(target=handle_request, args=(connection_socket,))
            thread.start()

        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break

    server_socket.close()
    sys.exit()


    
# printing a message to console which tells the server is listening on the specified host and port
print(f"Server is listening on {HOST}:{PORT}")

# creating a new thread, "thread_accept" and executing the main function
thread_accept = threading.Thread(target=receive)
thread_accept.start()