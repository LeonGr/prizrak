from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
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

            # print(r.content)
            # print(hashlib.sha512(r.content).hexdigest())
            # f = open("./deb/python-jellyfish-doc_0.8.2-1build2_all.deb", "rb")
            # content = f.read()
            # print(content)
            # self.wfile.write(content)
            # f.close()

            self.wfile.write(r.content)
        else:
            self.send_response(200)
            self.end_headers()
            f = open("." + self.path, "rb")
            content = f.read()
            # print(content)
            self.wfile.write(content)
            f.close()

if __name__ == "__main__":
    web_server = HTTPServer(("192.168.192.11", 80), Server)
    print("Server started")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped")
