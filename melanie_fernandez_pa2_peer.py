#Peer to peer, no central server

#Checklist
#Starts with username, local listening port, optional list of peer addresses
#While running, new connections must be accepted
#Any message must be broadcasted to all connected peers

import socket
import threading
import sys

def recv(socket: socket.socket, peers: set, lock: threading.Lock):
    buffer = "" #empty string for buffer

    try:
        while True:
            check = socket.recv(4096) #data recieved
            if not check:
                break
            buffer += check.decode("utf-8", errors = "replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(line) #Broadcast message to the connected peers

    except OSError:
        pass
    finally:
        #Lock is needed for multiple threads, preventing crash
        with lock:
            peers.discard(socket)
        try:
            socket.close()
        except OSError:
            pass

def accept_peer(listen_socket: socket.socket, peers: set, lock: threading.Lock):
    while True:
        try:
            conn, _ = listen_socket.accept() #connect incoming peer with no address needed
        except OSError:
            break
        with lock:
            peers.add(conn)
        threading.Thread(target=recv, args =(conn, peers, lock)).start()

def send_to_all(line: str, peers: set, lock: threading.Lock):
    data = line.encode("utf-8", errors = "replace")
    invalid = []
    with lock:
        for p in peers:
            try:
                p.sendall(data)
            except OSError:
                invalid.append(p)
            for p in invalid:
                peers.discard(p)
                try:
                    p.close()
                except OSError:
                    pass

def parse_peer(s: str):
    host, port_string = s.rsplit(':', 1) #standard indexing
    return host, int(port_string)

def main():
    if len(sys.argv) < 3:
        print("invalid arguments") #invalid connection
        sys.exit(1)

    username = sys.argv[1]
    listening_port = int(sys.argv[2])
    targets = sys.argv[3:]

    peers = set()
    lock = threading.Lock()

    listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_sock.bind(("127.0.0.1", listening_port))
    listening_sock.listen()

    threading.Thread(target=accept_peer, args=(listening_sock, peers, lock)).start() 

    for t in targets:
        try:
            host, port = parse_peer(t)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            with lock:
                peers.add(s)
            threading.Thread(target=recv, args=(s, peers, lock)).start()
        except OSError:
            pass

    try:
        while True:
            msg = input()
            line = f"[{username}]: {msg}\n"
            send_to_all(line, peers, lock)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        try:
            listening_sock.close()
        except OSError:
            pass
        with lock:
            for p in list(peers):
                try:
                    p.close()
                except OSError:
                    pass
            peers.clear()


if __name__ == "__main__":
    main()


