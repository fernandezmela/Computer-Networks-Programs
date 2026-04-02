#Server program from client-server
#Checklist:
#Multiple clients handled (multiple threads)
#Prints all recieved lines from clients
#Handles disconnects without crashing
#Line based messages through TCP

import socket
import threading
import sys

#Build up the centralized message distributor
#Parameters used to send message to clients
def broadcast(line: str, sender_socket: socket.socket, clients: set, clients_lock: threading.Lock):
    #Send message to all clients
    data = line.encode("utf-8", errors ="replace") #has to be bytes
    invalid = [] #List of broken sockets

    #Client lock allows for multiple clients
    with clients_lock:
        for s in clients:
            try:
                s.sendall(data) #Send message
            except OSError:
                invalid.append(s) #Anything sent not in bytes gets appended

        #remove dead sockets from the list and closes it
        for s in invalid:
            clients.discard(s)  # discard if data is invalid
            try:
                s.close()
            except OSError:
                pass


def manage_client(conn: socket.socket, address, clients: set, clients_lock: threading.Lock):
    #Requirement: recieves from client, newline, and broadcasts completed lines
    #initialize buffer
    buffer = ''

    try:
        while True:
            check = conn.recv(4096)
            if not check:
                #Disconnect
                break
            buffer += check.decode("utf-8", errors = "replace")

            #Extract newline terminated messages
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1) #regex hehe
                #Add a fully new line using broadcast
                #Call broadcast
                broadcast(line + "\n", conn, clients, clients_lock)

    #in the instance that the client drops connection
    except (ConnectionResetError, OSError):
        pass
    finally:
        with clients_lock:
            clients.discard(conn) #removes connection from client after abrupt disruption
        try:
            conn.close()
        except OSError:
            pass


def main():
    #Requirement: Server accepts a port number as a command line
    if len(sys.argv) != 2:
        print("invalid arguments")
        sys.exit(1)
    port = int(sys.argv[1])

    #Keep track of connected clients eith clients empty set
    clients = set()
    lock = threading.Lock()

    #"Welcome" = listening socket
    welcome = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Restart on the same port
    welcome.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #TCP connection
    welcome.bind(("127.0.0.1", port))
    welcome.listen()
    #terminal communication
    print(f"Server is listening on 127.0.0.1:{port}")

    try:
        #While clients are connected, begin threads (can have multiple threads)
        while True:
            conn, address = welcome.accept()
            with lock:
                clients.add(conn)
                #Begins sending and recieving via thread
            threading.Thread(
                target = manage_client,
                args=(conn, address, clients, lock),  #eg: localhost 5000
            ).start()

    except KeyboardInterrupt: #Standard keyboard interrupt
        pass
    finally: #close server
        with lock:
            for s in list(clients):
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()
        try:
            welcome.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()



                             
                             





           


          
