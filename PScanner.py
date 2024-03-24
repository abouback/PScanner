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
    target = socket.gethostbyname(sys.argv[1])  # Translate hostname to IPv4
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 PScanner.py <Target>")
    sys.exit()
    

# Add a pretty banner
print("-" * 65)
print("Scanning target "+target)
print("Time started: "+str(datetime.now()))
print("-" * 65)

# Add headers
print("{:<10} {:<10} {:<25}".format("PORT", "STATE", "SERVICE",  "VERSION" ))	 # It shows the header of the ports, state, service and version while scanning

try:
    # This is a try statement if the user wants to exit in the middle of the scanning
    for port in range(1, 101):  # Adjusted range to include port 65535
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) 	#set a shorter time while scanning
        #socket.setdefaulttimeout(1) 	#set the default time while scanning as 1
        result = s.connect_ex((target, port))  # Returns an error indicator
        
        #if result == 0:
            #service = get_service_name(port)   # This gives the service of the ports scanned
            #print("{:<10} {:<10} {:<25}".format(port, "Open", service))		# It gives the format in a neatly form starting with the ports, state and service
        #else:
            #print("{:<10} {:<10} {:<25}".format(port, "Closed", "N/A"))
        #s.close()
        
        if result == 0:
            service = socket.getservbyport(port)  # Get service name
            s.send(b"GET / HTTP/1.0\r\n\r\n")  # Send a basic HTTP request
            banner = s.recv(1024)  # Receive response
            version = banner.split(b'\r\n')[0]  # Extract version from banner
            print("{:<10} {:<10} {:<25} {:<30}".format(port, "Open", service, version.decode("utf-8")))  # Print port, state, service, and version
        s.close()
       
    # Exiting after finishing scanning the open ports
    print("\nScanning completed.")
    sys.exit()
    
except KeyboardInterrupt:  # Keyboard interrupt including the ctrl+c to cancel the scanning
    print("\nExiting.")
    sys.exit()

except socket.gaierror:  # If the host name could not be resolved, then exit
    print("Hostname could not be resolved.")
    sys.exit()

except socket.error:  # If the server could not connect, then exit
    print("Could not connect to server.")
    sys.exit()

