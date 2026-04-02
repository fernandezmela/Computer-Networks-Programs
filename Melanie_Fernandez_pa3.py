#Programming Assignment 3:
"Purpose: Minimal HTTP/1.1 Web Server"
"--> Persistent connection"
"--> Thread per connection using threading library"
"--> Get +Head for index.html/internet.jpg"

import os
import socket
import threading

#Build http response with status line, headers terminated, content length header
#Tells the browser how many bytes there are:
def build_response(status_line, headers, body, send_body = True):
   # REQUIREMENT: Content-Length must be exact byte size
    headers["Content-Length"] = str(len(body))

    response = status_line + "\r\n"

    # REQUIREMENT: All headers must end with \r\n
    for key in headers:
        response += key + ": " + headers[key] + "\r\n"

    # REQUIREMENT Blank line separating headers from body
    response += "\r\n"

    response_bytes = response.encode("utf-8")

    # For HEAD requests we do NOT send the body
    if send_body:
        response_bytes += body

    return response_bytes

#Handling HTTP Request:
def process_request(method, path, version, headers, body):
    #Extra credit: persistent connection

    #Looks inside the request header for the value of the header (retrived from the previous function)
    connection_header = headers.get("connection", "").lower()

    #Only keep alive if it says to, only close if it says to
    if version == "HTTP/1.0":
        keep_alive = (connection_header == "keep-alive")
    else:
        keep_alive = (connection_header != "close")

    close_connection = not keep_alive

    send_body = (method != "HEAD")

    #Post echo: for a single endpoint
    if method == "POST" and path == "/echo":
        if body is None:
            html = b"<h1>404 not found</h1>"
            return build_response("HTTP/1.1 400 Bad Request",
                {"Content-Type": "text/html; charset=utf-8",
                 "Connection": "close"},
                html,
                True
            ), True

        #request body
        text = body.decode("utf-8", errors="replace")

        html = (
        "<html><body>"
        "<h1>Echo</h1>"
        "<p>You posted:</p>"
        "<pre>" + text + "</pre>"
        "</body></html>"
        ).encode("utf-8")
           

        return build_response("HTTP/1.1 200 OK",
            {"Content-Type": "text/html; charset=utf-8",
             "Connection": "close" if close_connection else "keep-alive"},
            html,
            send_body
        ), close_connection
    
    #REQUIREMENT: Maps path to file:
    if path == "/" or path == "/index.html":
        filename = "index.html"
    elif path == "/internet.jpg":
        filename = "internet.jpg"
    else:
        html = b"<h1>404 not found</h1>"
        return build_response(
            "HTTP/1.1 404 Not Found",
            {"Content-Type": "text/html; charset=utf-8",
             "Connection": "close" if close_connection else "keep-alive"},
            html,
            send_body
        ), close_connection
    
    if not os.path.exists(filename):
        html = b"<h1> 404 not found</h1>"
        return build_response(
            "HTTP/1.1 404 Not Found",
            {"Content-Type": "text/html; charset=utf-8",
             "Connection": "close" if close_connection else "keep-alive"},
            html,
            send_body
        ), close_connection

    with open(filename, "rb") as f:
        file_data = f.read()

    if filename.endswith(".html"):
        content_type = "text/html; charset=utf-8"
    else:
        content_type = "image/jpeg"

    return build_response(
        "HTTP/1.1 200 OK",
        {"Content-Type": content_type,
         "Connection": "close" if close_connection else "keep-alive"},
        file_data,
        send_body
    ), close_connection

#REUQUIREMENT: Threading (in main will it thread per connection)
def handle_connection(conn):
    buffer = b""

    while True:
        while b"\r\n\r\n" not in buffer:
            data = conn.recv(4096)
            if not data:
                conn.close()
                return
            buffer += data

        header_part, buffer = buffer.split(b"\r\n\r\n", 1) #Requirment: splits

        try:
            header_text = header_part.decode("utf-8")
            lines = header_text.split("\r\n")

            request_line = lines[0]
            method, path, version = request_line.split()
        except:
            response = build_response(
                "HTTP/1.1 400 Bad Request",
                {"Content-Type": "text/html; charset=utf-8",
                 "Connection": "close"},
                b"<html><body><h1>400 Bad Request</h1></body></html>",
                True
            )
            conn.sendall(response)
            conn.close()
            return

        headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.lower()] = value.strip()

        body = None

        #Only if post, will you request the body
        if method == "POST":

            if "content-length" not in headers:
                response = build_response(
                    "HTTP/1.1 411 Length Required",
                    {"Content-Type": "text/html; charset=utf-8",
                     "Connection": "close"},
                    b"<html><body><h1>411 Length Required</h1></body></html>",
                    True
                )
                conn.sendall(response)
                conn.close()
                return

            length = int(headers["content-length"])

            while len(buffer) < length:
                buffer += conn.recv(4096)

            body = buffer[:length]
            buffer = buffer[length:]

        response, close_connection = process_request(
            method, path, version, headers, body
        )

        conn.sendall(response)

        if close_connection:
            conn.close()
            return

def main():
    if len(os.sys.argv) !=2:
        print("python3 melanie_fernandez_pa3.py <port>") #8080
        return
    
    port = int(os.sys.argv[1])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #REQUIREMENT: Bind to local host
    server.bind(("127.0.0.1", port))

    server.listen(5)

    print("Server running http://localhost:" + str(port)) #Gives you direct link to the port

    while True:
        conn, addr = server.accept()
        #REQURIRED: Threading per connection
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()

if __name__=="__main__":
    main()








