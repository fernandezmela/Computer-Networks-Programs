# Minimal HTTP Web Server (Python)

This project implements a simple HTTP/1.1 web server in Python using TCP sockets. The server accepts connections from a web browser, parses HTTP GET requests, and serves static files with properly formatted HTTP responses.

---

## Features

- Handles HTTP GET requests over TCP  
- Serves static files (`index.html`, `internet.jpg`)  
- Returns properly formatted HTTP/1.1 responses  
- Includes correct headers (Content-Length, Content-Type, Connection)  
- Supports multiple simultaneous connections using threading  
- Returns `404 Not Found` for invalid paths  

---

## How to Run

```bash
python3 firstname_lastname_pa3.py <port>
