#!/usr/bin/env python

import sys
import socket
from datetime import datetime

# Function to get service name for a port
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

# Defining our target
if len(sys.argv) == 2:
    target = sys.argv[1]
    try:
        target_ip = socket.gethostbyname(target)  # Translate hostname to IPv4
    except socket.gaierror:
        print(f"Hostname {target} could not be resolved.")
        sys.exit()
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 PScanner.py <Target>")
    sys.exit()

# Add a pretty banner
print("-" * 65)
print(f"Scanning target {target_ip}")
print(f"Time started: {datetime.now()}")
print("-" * 65)

# Add headers
print("{:<10} {:<10} {:<25} {:<30}".format("PORT", "STATE", "SERVICE", "VERSION"))  # Header for the output

try:
    # Scan all ports from 1 to 65535
    for port in range(1, 1025):  # Adjust the range for testing; use 65536 for a full scan
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set a timeout for each connection attempt
        result = s.connect_ex((target_ip, port))  # Returns an error indicator

        if result == 0:
            service = get_service_name(port)  # Get service name
            try:
                s.send(b"GET / HTTP/1.0\r\n\r\n")  # Send a basic HTTP request
                banner = s.recv(1024)  # Receive response
                version = banner.split(b'\r\n')[0]  # Extract version from banner
                print("{:<10} {:<10} {:<25} {:<30}".format(port, "Open", service, version.decode("utf-8", errors='ignore')))  # Print port, state, service, and version
            except Exception as e:
                print("{:<10} {:<10} {:<25} {:<30}".format(port, "Open", service, "No version info"))
        s.close()

    # Exiting after finishing scanning the open ports
    print("\nScanning completed.")

except KeyboardInterrupt:  # Keyboard interrupt to cancel the scanning
    print("\nExiting.")
    sys.exit()

except socket.gaierror:  # If the host name could not be resolved, then exit
    print("Hostname could not be resolved.")
    sys.exit()

except socket.error as e:  # If the server could not connect, then exit
    print(f"Could not connect to server: {e}")
    sys.exit()

