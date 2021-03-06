#!/usr/bin/python
import socket
import time
import random

# Variables
IPIFACE = "8.8.8.8"
PORT = 12347
BUF = b'x' * random.randint(800,1500)
BLOCKING = 0
SLEEP = True
SLEEPTIME = 0.00025
PRINT = True

# Main
i = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.setblocking(BLOCKING)
sock.setsockopt(socket.SOL_IP, socket.IP_TTL, 4)
sock.connect((IPIFACE, PORT))
while True:
	try:		
		sock.send(BUF)
		if SLEEP:
			time.sleep(SLEEPTIME)
	except socket.error, e:
		# don't print to keep pumping data
		if PRINT:
			print "Socket Error occurred %s: %s" % (i, e)
                        i += 1
		pass
