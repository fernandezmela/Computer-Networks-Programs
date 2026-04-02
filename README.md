# Reliable Data Transfer over UDP

This project implements a reliable data transfer protocol on top of UDP in Python. The goal is to replicate core reliability mechanisms—such as sequencing, acknowledgments, retransmissions, and sliding windows—without using TCP.

The system ensures correct file transfer between a sender and receiver, even in the presence of packet loss.

---

## Features

- Reliable file transfer over UDP  
- Sliding window protocol (Go-Back-N style)  
- Sequence numbers and cumulative acknowledgments  
- Retransmission on timeout  
- Receiver-side buffering of out-of-order packets  
- Packet loss simulation for testing robustness  
- Performance metrics (retransmissions, transfer time, throughput)  

---

## How to Run

### Receiver
```bash
python3 firstname_lastname_receiver.py <listen_port> <output_filename> <loss_probability>
