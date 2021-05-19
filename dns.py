from scapy.all import *

# iface = "enp0s3"
iface = "enp7s0"

def dns_sniff(packet):
    if (packet.haslayer(DNS)):
        print("DNS request for IP: " + str(packet.summary()))
        try:
            packet = modify_packet(packet)
        except IndexError:
            pass
        print("Modified request for IP: " + str(packet.summary()))
    # sendp(packet, iface)

def modify_packet(packet):
    return packet

sniff(count = 0, filter = "port 53", prn = dns_sniff, iface=iface)
