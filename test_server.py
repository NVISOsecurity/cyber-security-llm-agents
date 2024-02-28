import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


class CustomHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, HTTP!")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        print(post_data.decode())
        self.send_response(200)
        self.end_headers()


def print_server_interfaces(port):
    print(f"Server running on port {port}...")
    hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(hostname)
    for ip_address in ip_addresses[2]:
        if ip_address != "127.0.0.1":
            print(f"Listening on interface: {ip_address}:{port}")


def run(server_class=HTTPServer, handler_class=CustomHTTPHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print_server_interfaces(port)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
