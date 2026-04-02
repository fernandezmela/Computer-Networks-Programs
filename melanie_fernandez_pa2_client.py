#Client: Client server program
#Checklist:
#Connect to server using TCP
#Client is usually requesting and recieving
#Send what the user wants to the server
#Recieve messages from the server as they arrive
#Do the following concurrently

#Two main functions:
#input() --> sendall()
#recv() --> print()

import socket
import threading
import sys

def send(socket: socket.socket, username: str):
    try:
        #Main loop
        while True:
            msg = input()
            #new line message boundary is necessary, makes it look clean
            line = f"[{username}]: {msg}\n" #messages must have this format eg: Jim: hello
            socket.sendall(line.encode("utf-8", errors = "replace"))
    except (EOFError, KeyboardInterrupt, OSError): #socket issues, closes socket with the following conditions
        pass
    finally:
        try:
            socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            socket.close()
        except OSError:
            pass


def recieve(socket: socket.socket):
    buffer = ''
    try:
        while True:
            check = socket.recv(4096)  #recieves data from the network --> gives 4096 bytes at a time
            if not check:
                break #breaks if the socket is empty and there are no bytes
            buffer += check.decode("utf-8", errors = 'replace')

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1) #new line split
                print(line)
    except OSError:
        pass
    finally:
        try:
            socket.close()
        except OSError:
            pass


def main():
    #requirement: accept hostname , port, username
    if len(sys.argv) not in (3, 4):
        print("invalid arguments")
        sys.exit(1) #Program ending due to an error (program running incorrectly)

    #Parse host, port, and username
    host = sys.argv[1]
    port = int(sys.argv[2])

    if len(sys.argv) == 4:
        username = sys.argv[3]
    else:
        username = input("Username: ").strip() or "anon"  # FIX: username must exist

    #TCP socket and connect (TCP --> AF_INET, SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TODO: change client to client_socket
    client_socket.connect((host, port))

    #Thread for client: allowing for sending recieving
    threading.Thread(target=recieve, args=(client_socket,)).start()  # TODO
    send(client_socket, username) 


if __name__ == "__main__":
    main()



