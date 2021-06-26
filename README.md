# Призрак

Призрак (pronounced "prizrak"), Bulgarian for "Ghost", is a project that attemps to install malware on Ubuntu machines through the `apt` package manager. 
This is done by using a Man-in-the-Middle (MitM) attack to divert requests for Ubuntu mirror servers to an imposter web server. This server injects malicious code into the `preinst` file of the requested `.deb` archive.
However, `apt`'s use of checksums prevent the full attack from working. 

### Dependencies:
* python3.6 (NetfilterQueue does not work with higher versions)
* [Scapy](https://scapy.net/) (utilities, packet creation and modification)
* [NetfilterQueue](https://pypi.org/project/NetfilterQueue/) (interaction with packets in the NFQUEUE)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (scraping Ubuntu mirrors)

### Usage

`sudo ./prizrak.py -t <Target_IP> -g <Gateway_IP> -i <Interface>`

### Implementation

`prizrak.py` starts three threads:
* `arp_spoof` from `arp.py`, which poisons the ARP cache table of the target and the gateway to initiate a MitM attack.
* `dns_spoof` from `dns.py`, which poisons the victim's DNS cache so traffic to Ubuntu mirror servers gets redirected to the attacker's machine.
* `start_server` from `fake_server.py`, which creates a webserver which accepts requests for `apt` packages and injects the code from `malware/install`.

Upon installation of the package, three files are downloaded:
* `malware/l32`, an executable which starts a bind shell on port 65123.
* `malware/systemd-helper.service`, a `systemd` service which restarts `l32` on reboot/crash.
* `malware/libc.lib32.so.6`, a shared library which gets added to `/etc/ld.so.preload` to overwrite the `fopen`, `fopen64`, `readdir`, `readdir64`, and `statx` functions.

The shared library hides the downloaded files from `ls` and additionally hides the opened port from programs such as `netstat` which use `/proc/net/tcp` to get information about active TCP connections.
