from scapy.all import *

def dns_sniff(pakket):
    if (pakket.haslayer(DNS)):
        print("DNS request for IP: " + str(pakket.summary()))

iface = "enp0s3"
sniff(count = 0, filter = "port 53", prn = dns_sniff, iface=iface)
