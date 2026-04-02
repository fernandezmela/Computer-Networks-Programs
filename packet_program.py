#Melanie Fernnadez

#Builds a quantative model of Internet performance using the concepts of packet switching, store-and-forward, transmission delay, bottlenecks, and throughput
import math 

#Given Parameters:
File_bytes = 5 * (2 ** 20)
Payload_sizes = [700, 1400, 2800] 
Header_bytes = 100  

#Path (3 links)
Rates_bps = [10e6, 5e6, 20e6] # 10000000, 5000000, 20000000
Propogation = [10e-3, 20e-3, 5e-3] #Seconds


#Part A
def compute_payload(payload_bytes):
    #Conversion file size bits for throughput and delay calculations
    File_bits = File_bytes * 8
    P = math.ceil(File_bytes / payload_bytes)

    #Header and payload in bits (*8)
    L = (payload_bytes + Header_bytes) * 8
    dtrans = [L / Ri for Ri in Rates_bps] #transimssion delay per link

    Tfirst = sum(dtrans[i] + Propogation[i] for i in range(3)) 

    #Bottleneck transfer
    delay_dtrans = max(dtrans)
    Tfile = Tfirst + (P - 1) * delay_dtrans

    throughput_bps = File_bits / Tfile
    throughput_mbps = throughput_bps / 1e6

    utilizations = [throughput_bps / Ri for Ri in Rates_bps]

    return P, L, Tfirst, Tfile, throughput_mbps, delay_dtrans, utilizations


def main():
    for payload in Payload_sizes:
        P, L, Tfirst, Tfile, thr_mbps, delay_dtrans, utils = compute_payload(payload)

        print("payload_bytes:", payload)
        print("num_packets:", P)
        print("packet_size_bits:", L)
        print("first_packet_arrival_s:", round(Tfirst, 6))
        print("file_arrival_s:", round(Tfile, 6))
        print("throughput_mbps:", round(thr_mbps, 6))
        print("delay_dtrans_s:", round(delay_dtrans, 6))
        print("link_utilizations:", [round(u, 6) for u in utils])
        print()

if __name__ == "__main__":
    main()

