# Internet Performance Model

This project builds a simple quantitative model of Internet performance using core networking concepts such as packet switching, store-and-forward transmission, transmission delay, propagation delay, bottlenecks, throughput, and link utilization.

The program analyzes how a file is packetized and transmitted across a 3-link path, then computes end-to-end performance under different packet payload sizes.

## Features

- Computes packetization for a fixed file size
- Calculates transmission and propagation delays per link
- Models first-packet end-to-end delay with store-and-forward forwarding
- Computes full file arrival time with pipelining
- Identifies bottleneck link behavior
- Calculates effective throughput and per-link utilization
- Compares performance for multiple payload sizes

## Scenarios Studied

The model evaluates payload sizes of:

- 700 bytes
- 1400 bytes
- 2800 bytes

For each case, it reports:

- `payload_bytes`
- `num_packets`
- `packet_size_bits`
- `first_packet_arrival_s`
- `file_arrival_s`
- `throughput_mbps`
- `bottleneck_mbps` or bottleneck transmission delay
- `link_utilizations`

## How to Run

```bash
python firstname_lastname_pa1.py
