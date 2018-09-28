#!/usr/bin/python
import socket
import sys

#create an INET, DGRAM socket
serversock = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM)
#bind the socket to a public host,
# and a well-known port
server_address = ("192.168.1.113", 1111)
serversock.bind(server_address)
print >>sys.stderr, 'Starting Echo Server on %s port %s' % server_address
while True:
	data, address = serversock.recvfrom(4096)
	if data:
        	sent = serversock.sendto(data, address)
		print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
