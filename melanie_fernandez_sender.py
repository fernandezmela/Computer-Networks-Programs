#Sender program --> Programming Assignment 4

import sys
import time
import socket
import struct

#Packet format
data_header = 6 #4 bytes + 2
#Creating packet using struct with no text based encoding
data_header = 6 #4 bytes + 2
def packet_size(seq_num, payload):
    header = struct.pack(">IH", seq_num, len(payload))
    return header + payload

#Ack format
ack_size = 4 #4 bytes
def ack(ack_num):
    return struct.pack(">I", ack_num)

def unpack_ack(raw_bytes):
    if len(raw_bytes) < ack_size:
        return None
    ack_num, = struct.unpack(">I", raw_bytes[0:4])
    return ack_num

#MTU
max_payload = 1000
timeout = 0.5 #in seconds

def chop_file(data, chopped_size=max_payload):
    chopped = [] #Empty list initializing parts of the data
    offset = 0
    while offset < len(data):
        chopped.append(data[offset : offset + chopped_size])
        offset += chopped_size
    return chopped

def segment(sock, addr, seq_num, payload):
    pkt = packet_size(seq_num, payload)
    sock.sendto(pkt, addr)

#Standard read file
def run_sender(reciever_host, reciever_port, input_filename, window_size):
    with open(input_filename, 'rb') as f:
        file_data = f.read()

    file_size = len(file_data)
    segments = chop_file(file_data)
    total_segs = len(segments)

    print(f'sender file size = {file_size} bytes')
    print(f'sender segments = {total_segs}')
    print(f'sender window size = {window_size}')
    print(f'sender timeout = {timeout} seconds')

    #retrieve information and send information from socket
    receiver_addr = (reciever_host, reciever_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    #Empty starting values to send packets
    base = 0
    next_send = 0
    retransmissions = 0
    start_time = time.time()

    #Chops the file into 1000 byte chunks and sends them with the size of the sliding window
    while base < total_segs:
        #Window
        while next_send < base + window_size and next_send < total_segs:
            segment(sock, receiver_addr, next_send, segments[next_send])
            print(f"sender sent seq={next_send}")
            next_send += 1

        try:
            raw, _ = sock.recvfrom(2048)

            if raw == bytes([255]):
                break

            ack_num = unpack_ack(raw)
            if ack_num is None:
                continue

            print(f"sender recieved ACK = {ack_num} (base = {base})")

            if ack_num > base:
                base = ack_num

        except socket.timeout:
            print(f"sender ** timeout ** retransmitting seq {base} to {next_send - 1}")
            for seq in range(base, next_send):
                segment(sock, receiver_addr, seq, segments[seq])
                retransmissions += 1
                print(f"sender retransmit seq = {seq}")

    #Send FIN
    for i in range(10):
        sock.sendto(bytes([255]), receiver_addr)
        try:
            raw, _ = sock.recvfrom(16)
            if raw == bytes([255]):
                print("sender received ACK, now closing")
                break
        except socket.timeout:
            pass

    end_time = time.time()
    elapsed = end_time - start_time
    throughput = file_size / elapsed

    print(f"retransmissions = {retransmissions}")
    print(f"transfer time = {elapsed:.2f} seconds")
    print(f"effective throughput = {throughput:.2f}")
    sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: python3 melanie_fernandez_sender.py " "<receiver_host> <receiver_port> <input_filename> <window_size>")
        sys.exit(1)

    #indexing for terminal print
    receiver_host = sys.argv[1]
    receiver_port = int(sys.argv[2])
    input_filename = sys.argv[3]
    window_size = int(sys.argv[4])

    if window_size < 1:
        print('Error: window_size must be 1 or more')
        sys.exit(1)

    run_sender(receiver_host, receiver_port, input_filename, window_size)