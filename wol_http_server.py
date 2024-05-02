import argparse
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

WOL_DEVICE_MAC_ADDR = 'YOUR_DEVICES_MAC_ADDR_HERE'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Wake-On-LAN</title>
                </head>
                <body>
                    <button onclick="fetch('/trigger_wol')">Power On Device</button>
                </body>
                </html>
            ''')
        elif self.path == '/trigger_wol':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            try:
                result = subprocess.run(['./wakeonlan', WOL_DEVICE_MAC_ADDR], capture_output=True, text=True)
                output = result.stdout
                self.wfile.write(f'System program executed successfully. Output: {output}'.encode('utf-8'))
            except Exception as e:
                self.wfile.write(f'Error executing system program: {str(e)}'.encode('utf-8'))
        else:
            self.send_error(404)

def main():
    parser = argparse.ArgumentParser(description='Run a web server with an endpoint to execute a system program.')
    parser.add_argument('--port', type=int, default=8000, help='Port number for the web server (default: 8000)')
    args = parser.parse_args()

    server_address = ('', args.port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {args.port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()

