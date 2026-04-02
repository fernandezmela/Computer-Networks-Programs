# Networked Chat Application (TCP)

This project implements a simple terminal-based chat application in Python using TCP sockets. The application is built in two different architectures to demonstrate how communication models impact system design:

- Client–Server Architecture  
- Peer-to-Peer (P2P) Architecture  

The goal of this project is to explore socket-level communication, concurrency, and application design in networked systems.

---

## Features

- Real-time text-based chat over TCP  
- Two implementations: client–server and peer-to-peer  
- Concurrent handling of user input and incoming messages  
- Robust message handling using newline-delimited streams  
- Terminal-based interface (no GUI required)

---

## Key Concepts

- TCP socket programming using Python’s `socket` module  
- Concurrent I/O handling using threading (or `select`)  
- Stream-based message parsing (handling partial `recv()` data)  
- Comparison of centralized vs decentralized network architectures  

---

## ⚙️ Implementation Details

- Messages are sent as newline-terminated strings  
- Incoming data is buffered and parsed into complete messages  
- Each program instance handles:
  - user input (sending messages)
  - network input (receiving messages)

- Threads are used to allow simultaneous:
  - reading from standard input  
  - listening on sockets  

---

## Architectures

### Client–Server
- A central server handles all message routing  
- Clients connect to the server and send/receive messages  

### Peer-to-Peer
- No central server  
- Each peer connects directly to other peers  
- Messages are exchanged directly between participants  

---

## How to Run

### Client–Server Version

Start the server:
```bash
python server.py <port>

