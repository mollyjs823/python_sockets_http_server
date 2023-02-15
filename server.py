import socket
from pathlib import Path
import sys

server_port = 80
if len(sys.argv) > 1:
    try:
        server_port = int(sys.argv[1])
    except ValueError:
        print("Invalid port")
        sys.exit(1)


# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ''
# Bind socket to a specific address and port
s.bind((server_addr, server_port))

# Listen on the port
s.listen(1)

while True:
    try:
        # Accept a new connection / listen for incoming requests
        client_s, client_addr = s.accept()

        # Wait for request
        msg = client_s.recv(2048)
        parsedMsg = msg.decode('ascii')
        # Parse request 
        for line in parsedMsg.splitlines():
            if line[0:3] == 'GET':
                file = "." + line.split()[1]
                break

        # Get file from server's file system
        path = Path(file)
        if not path.is_file():
            file_data = ""
            response_status = '404'
            response_status_text = 'Not Found'
        else:
            file_data = open(file, 'r').read()
            response_status = '200'
            response_status_text = 'OK'

        # Send response with file and headers
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(file_data),
            'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())
        
        response_proto = 'HTTP/1.1'
        client_s.send(('%s %s %s' % (response_proto, response_status, response_status_text)).encode('ascii'))
        client_s.send('\n'.encode('ascii'))
        client_s.send(response_headers_raw.encode('ascii'))
        client_s.send('\n'.encode('ascii'))
        client_s.send(file_data.encode('ascii'))
    except KeyboardInterrupt:
        print("Server socket closing")
        break
    finally:
        client_s.close()

s.close()


