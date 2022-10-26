# Program Name: port_scanner.py

# Import necessary module
import os
import socket
import argparse
from datetime import datetime
import sys

default_ports = ["21","22","23","25","53","80","110","111","135","139","143","443","445","993","995","1723","3306","3389","5900","8080"]

parser = argparse.ArgumentParser(
    description='CLI based script for network port scanner using Python3. '
    'You can either user -p for list of ports specified or -s to provide range of ports. ' 
    'If none is provided it will scan through list of common ports.',
    epilog='Examples: '
    'python3 port_scanner.py -r 192.168.1.1 -p 21 22 23 25 -b'
)

port_group = parser.add_mutually_exclusive_group()

parser.add_argument('-r','--rhost', type=str, default='127.0.0.1',
                    help='Remote Host IP Address. Default: 127.0.0.1')
port_group.add_argument('-p','--port', nargs="?", default=default_ports, 
                    help='Input port number to scan or range of port number. Eg. 20 80')
port_group.add_argument('-s','--range', nargs=2, type=int,
                    help='Input start and end port number to scan. Eg. 20 80')
parser.add_argument('-b','--banner', action="store_true",
                    help='Use this flag to get banner information')

parser_args = parser.parse_args()

remote_host = parser_args.rhost
ports = parser_args.port
ports_range = parser_args.range
banner = parser_args.banner

# If user selects the range option. Replace the default ports and use range instead
if ports_range != None:
    ports = list(range(ports_range[0], ports_range[1]+1))

# Resolve the host name from entered IP Address.
try:
    host_name = socket.gethostbyaddr(remote_host)
except:
    pass

# Add Banner
print("-" * 50)
print("Scanning Target: " + remote_host)
if host_name != '':
    print("Host Name: " + host_name[0])

print("Scanning started at: " + str(datetime.now()))
print("-" * 50)

# Socket used to connect to remote host and port
try:
     
    # will scan ports in the list
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
         
        # returns an error indicator
        result = s.connect_ex((remote_host,int(port)))
        if result == 0:
            # Checks if banner flag is set to true
            if banner:
                try:
                    # Get the banner information
                    banner = s.recv(1024).decode()
                    print("Port: {} is open with banner: {}".format(port, banner))
        
                except:
                    print("Port: {} is open ".format(port))
            else:
                print("Port: {} is open ".format(port))

        s.close()
         
except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()