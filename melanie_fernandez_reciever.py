import socket
import random
import sys
import struct

data_header = 6 #4 bytes + 2
ack_size = 4 #4 bytes
payload = 1000 #as mentioned in instructions

def packet_size(seq_num, payload):
    header = struct.pack(">IH", seq_num, len(payload))
    return header + payload

#Ack format
#Construct and deconstruct acks using struct
ack_size = 4 #4 bytes
def ack(ack_num):
    return struct.pack(">I", ack_num)

def unpack_ack(raw_bytes):
    if len(raw_bytes) < data_header:
        return None
    seq_num, pay_len = struct.unpack(">IH", raw_bytes[0:6]) #cuts the packet into chunks
    payload = raw_bytes[data_header: data_header + pay_len]
    return seq_num, payload
   

#Socket setup
def receiver(listen_port, output_filename, loss_prob):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", listen_port))
    print(f"reciever listening on UDP port {listen_port}")
    print(f"reciever loss probablity = {loss_prob:.2f}") #.2f (2 numbers after the decimal)
    print(f"reciever output file = {output_filename}")

    #The three things we need to track
    next_expected = 0 #ACK pointer
    buffer = {} #Holds segments
    sender_addr = None #Allows us to ACK back
    output_data = bytearray() #array of file data

    #Main Loop
    #In the main loop, after every iteration we recieve and potentially drop
    done = False
    while not done:
        #Blocks until a UDP datagram arrives
        raw, addr = sock.recvfrom(2048)

        #Recalls the senders addr
        if sender_addr is None:
            sender_addr = addr

        #Loss: No ack is sent if the packet is lost
        if random.random() < loss_prob:
            print(f"reciever (dropped packet)")
            continue

        if raw == bytes([255]):
            print("receiver -- transfer complete")
            sock.sendto(bytes([255]), sender_addr)
            done = True
            break

        #Unpack the header and store the segment
        result = unpack_ack(raw)
        if result is None:
            continue

        seq_num, payload = result
        print(f"receiver got seq={seq_num}  len={len(payload)}  next_expected={next_expected}")

        if seq_num >= next_expected:
            buffer[seq_num] = payload

            # Drain contiguous segments into output
            while next_expected in buffer:
                output_data.extend(buffer.pop(next_expected))
                next_expected += 1

        # Send cumulative ACK — always, even for duplicates
        sock.sendto(ack(next_expected), sender_addr)
        print(f"receiver sent ACK = {next_expected}")

    with open(output_filename, 'wb') as f:
        f.write(output_data)
    print(f"reciever wrote- {len(output_data)} bytes to '{output_filename}'")
    sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 firstname_lastname_receiver.py "
              "<listen_port> <output_filename> <loss_probability>")
        sys.exit(1)

    #Indexes for terminal output
    listen_port     = int(sys.argv[1])
    output_filename = sys.argv[2]
    loss_prob       = float(sys.argv[3])

    if not (0.0 <= loss_prob < 1.0):
        print("Error: loss_probability must be in [0.0, 1.0)")
        sys.exit(1)

    receiver(listen_port, output_filename, loss_prob)