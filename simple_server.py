#!/usr/bin/env python3
"""
Utility to create a simple HTTP(s) server for testing purpose.
SSL certificate: openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
import ssl
import logging
import argparse


class SimpleServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(port, connection, keyfile, certfile, server_class=HTTPServer, handler_class=SimpleServer):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    if connection == 'https':
    	httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=keyfile, certfile=certfile, server_side=True)
    
    logging.info('httpd Server Started...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info('Exception: unable to start httpd server...\n')
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='''Utility to create a simple HTTP(s) server that log incoming requests for testing purposes.
		For now, it supports GET and POST methods.''',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-t", "--type", choices=["http","https"], type=str, help="create a server with http or https capabilities",
		default="http")
	parser.add_argument("-p", "--port", type=int, help="define server port", default=4444)
	parser.add_argument("-k", "--key", help="path to keyfile (required for SSL)", default='./key.pem')
	parser.add_argument("-c", "--cert", help="path to certificate file (required for SSL)", default='./cert.pem')
	
	args = parser.parse_args()
	run(port=args.port,connection=args.type, keyfile=args.key, certfile=args.cert)